from fastapi import FastAPI, UploadFile, Form
from agentic_agent import run_agent   # <-- yahan se proper import

app = FastAPI()

@app.post("/recommend")
async def recommend(file: UploadFile = None, text: str = Form(...)):
    image_path = None

    # If user uploaded image
    if file:
        image_path = f"temp_{file.filename}"
        with open(image_path, "wb") as f:
            f.write(await file.read())

    # Call your agent function
    result = run_agent(text, image_path)

    return {"response": result}

