from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import traceback
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agentic_agent import run_agent
except ImportError as e:
    print(f"❌ Failed to import agentic_agent: {e}")
    print("Make sure agentic_agent.py is in the same directory")
    sys.exit(1)

app = FastAPI(title="Restaurant Finder API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "ok",
        "message": "Restaurant Finder API is running",
        "endpoints": {
            "recommend": "/recommend (POST)",
            "docs": "/docs"
        }
    }

@app.post("/recommend")
async def recommend(
    text: str = Form(...),
    city: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Main recommendation endpoint
    
    Args:
        text: Search query (required)
        city: Preferred city (optional)
        file: Food image (optional)
    
    Returns:
        JSON with llm_output and scraped_data
    """
    
    print("\n" + "="*60)
    print("📥 NEW REQUEST")
    print("="*60)
    print(f"📝 Text: {text}")
    print(f"🌆 City: {city}")
    print(f"📷 File: {file.filename if file else 'None'}")
    print("="*60)
    
    image_path = None
    
    # Handle file upload
    if file:
        try:
            image_path = f"temp_{file.filename}"
            print(f"💾 Saving image to: {image_path}")
            
            content = await file.read()
            with open(image_path, "wb") as f:
                f.write(content)
            
            print(f"✅ Image saved ({len(content)} bytes)")
            
        except Exception as e:
            error_msg = f"Failed to save image: {str(e)}"
            print(f"❌ {error_msg}")
            traceback.print_exc()
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": error_msg,
                    "type": "file_upload_error"
                }
            )
    
    # Run the agent
    try:
        print(f"\n🤖 Starting agent...")
        
        result = run_agent(
            user_text=text,
            image_path=image_path,
            preferred_city=city
        )
        
        print(f"✅ Agent completed!")
        
        # Validate result structure
        if not isinstance(result, dict):
            raise ValueError(f"Agent returned invalid type: {type(result)}")
        
        if "llm_output" not in result:
            print("⚠️ Warning: No llm_output in result")
            result["llm_output"] = "No recommendations available"
        
        if "scraped_data" not in result:
            print("⚠️ Warning: No scraped_data in result")
            result["scraped_data"] = []
        
        scraped_count = len(result.get("scraped_data", []))
        print(f"📊 Results: {scraped_count} restaurants found")
        print("="*60 + "\n")
        
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except Exception as e:
        error_msg = f"Agent failed: {str(e)}"
        print(f"\n❌ ERROR: {error_msg}")
        print("="*60)
        traceback.print_exc()
        print("="*60 + "\n")
        
        return JSONResponse(
            status_code=500,
            content={
                "error": error_msg,
                "type": "agent_error",
                "traceback": traceback.format_exc()
            }
        )
    
    finally:
        # Clean up temp image
        if image_path and os.path.exists(image_path):
            try:
                import time
                time.sleep(0.1)  # Small delay for Windows file handle release
                os.remove(image_path)
                print(f"🗑️ Cleaned up: {image_path}")
            except PermissionError:
                print(f"⚠️ Could not delete {image_path} - file in use (will be cleaned up later)")
            except Exception as e:
                print(f"⚠️ Failed to delete temp file: {e}")

@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        # Test import
        from agentic_agent import run_agent
        agent_status = "✅ OK"
    except Exception as e:
        agent_status = f"❌ Error: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "Restaurant Finder API",
        "agent_import": agent_status
    }

# For testing
if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Restaurant Finder API...")
    print("📍 URL: http://127.0.0.1:8000")
    print("📖 Docs: http://127.0.0.1:8000/docs")
    print("\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)


