import streamlit as st
import requests
import json

# Page config
st.set_page_config(
    page_title="Restaurant Finder",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .restaurant-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 15px;
        border-left: 4px solid #ff4b4b;
    }
    .restaurant-name {
        font-size: 20px;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 8px;
    }
    .restaurant-info {
        font-size: 14px;
        color: #555;
        line-height: 1.6;
    }
    .ai-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0068c9;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Restaurant Finder")
st.markdown("*Discover the best restaurants in Pakistan*")

# Input fields
col1, col2 = st.columns([1, 2])

with col1:
    cities = ["Lahore", "Karachi", "Islamabad", "Faisalabad", "Murree"]
    selected_city = st.selectbox("🌆 Select City", cities, index=2)

with col2:
    text_input = st.text_input(
        "🔍 What are you looking for?", 
        placeholder="e.g., loaded fries, biryani, pizza"
    )

uploaded_file = st.file_uploader("📸 Upload dish image (optional)", type=["jpg", "png", "jpeg"])

# Search button
if st.button("🔍 Find Restaurants", type="primary", use_container_width=True):
    if not text_input:
        st.warning("⚠️ Please enter what you're looking for!")
    else:
        with st.spinner(f"🔎 Searching restaurants in {selected_city}..."):
            
            # Prepare form data
            data = {
                "text": text_input,
                "city": selected_city.lower()
            }
            
            files = None
            if uploaded_file:
                # Reset file pointer
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            
            try:
                # Make API request
                response = requests.post(
                    "http://127.0.0.1:8000/recommend",
                    data=data,
                    files=files,
                    timeout=90
                )
                
                # Check status code
                if response.status_code != 200:
                    st.error(f"❌ Server error (Status: {response.status_code})")
                    with st.expander("Show error details"):
                        st.code(response.text)
                    st.stop()
                
                # Parse JSON response
                try:
                    result_json = response.json()
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON response from server")
                    with st.expander("Show raw response"):
                        st.code(response.text[:1000])
                    st.stop()
                
                # Extract data (handle both nested and direct structure)
                if "response" in result_json:
                    actual_data = result_json["response"]
                else:
                    actual_data = result_json
                
                # Check for error in response
                if "error" in actual_data:
                    st.error(f"❌ {actual_data['error']}")
                    st.stop()
                
                # Get results
                llm_output = actual_data.get("llm_output", "")
                scraped_data = actual_data.get("scraped_data", [])
                
                # Display AI recommendations
                if llm_output:
                    st.markdown("## 🤖 AI Recommendations")
                    st.markdown(f'<div class="ai-box">{llm_output}</div>', unsafe_allow_html=True)
                
                # Display all restaurants in one section
                st.markdown(f"## 🔍 Found {len(scraped_data)} Restaurant(s)")
                
                if scraped_data and len(scraped_data) > 0:
                    no_results = scraped_data[0].get("name") == "⚠️ No restaurants found"
                    
                    if not no_results:
                        for idx, item in enumerate(scraped_data, 1):
                            # Extract rating from description if available
                            rating_display = "⭐ Not rated"
                            desc = item.get('description', '')
                            
                            # Try to find rating in description
                            if 'rating' in desc.lower() or 'review' in desc.lower():
                                # Extract numbers before "reviews"
                                import re
                                rating_match = re.search(r'(\d+\.?\d*)\s*\((\d+)\s*reviews?\)', desc)
                                if rating_match:
                                    rating_display = f"⭐ {rating_match.group(1)}/5 ({rating_match.group(2)} reviews)"
                            
                            st.markdown(f"""
                            <div class="restaurant-card">
                                <div class="restaurant-name">
                                    {idx}. {item.get('name', 'Unknown Restaurant')}
                                </div>
                                <div class="restaurant-info">
                                    📍 <strong>Location:</strong> {item.get('location', 'N/A')[:100]}<br>
                                    ⭐ <strong>Rating:</strong> {rating_display}<br>
                                    🌆 <strong>City:</strong> {item.get('city', 'N/A')}<br>
                                    💬 {item.get('description', 'No description')[:250]}...
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("")  # Small spacing
                    else:
                        st.warning("⚠️ No restaurants found. Try different keywords!")
                else:
                    st.info("No results returned from search.")
            
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout! Server took too long to respond.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to backend!")
                st.info("Make sure FastAPI is running:\n```\nuvicorn main:app --reload\n```")
            except Exception as e:
                st.error(f"❌ Unexpected error: {type(e).__name__}")
                with st.expander("Show error details"):
                    st.code(str(e))

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    ### Quick Start:
    1. Select your city
    2. Enter what you're looking for (e.g., "loaded fries", "biryani")
    3. Optionally upload a food image
    4. Click "Find Restaurants"
    
    ### Tips:
    - Be specific: "DHA loaded fries" > "fries"
    - Try: "chinese food", "italian", "desi breakfast"
    - Include areas: "F7 cafes", "Gulberg restaurants"
    """)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Status")
    
    # Test backend
    try:
        health = requests.get("http://127.0.0.1:8000/", timeout=2)
        if health.status_code == 200:
            st.success("✅ Backend Online")
        else:
            st.warning("⚠️ Backend Issues")
    except:
        st.error("❌ Backend Offline")
        st.code("uvicorn main:app --reload")
    
    st.markdown("### 🎯 Recent Searches")
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if text_input and text_input not in [h.split('-')[0].strip() for h in st.session_state.history]:
        st.session_state.history.insert(0, f"{text_input} - {selected_city}")
        if len(st.session_state.history) > 5:
            st.session_state.history.pop()
    
    for h in st.session_state.history[:5]:
        st.text(f"• {h}")


