import streamlit as st
import requests

st.title("Restaurant Finder")

uploaded_file = st.file_uploader("Upload dish image", type=["jpg", "png"])
text_input = st.text_input("Enter your preferences")

if st.button("Find Restaurants") and uploaded_file and text_input:
    # File saving logic is fine
    path = f"temp_{uploaded_file.name}"
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())

    try:
        # Request logic is fine
        with open(path, "rb") as file_data:
            files = {"file": file_data}
            data = {"text": text_input}
            response = requests.post("http://127.0.0.1:8000/recommend", files=files, data=data)

        # 1. Response JSON ko load karein
        result_json = response.json()

        # 2. FastAPI se aayi hui 'response' key ko extract karein
        agent_result = result_json.get("response")

        st.write("### Recommended Restaurants:")

        # -------------- 🟢 NEW CLEAN DISPLAY LOGIC -----------------
        if isinstance(agent_result, list):  # If list of dicts
            for item in agent_result:
                st.markdown(f"""
                **{item.get('name', 'N/A')}**  
                📍 *{item.get('location', 'Unknown')}*  
                ⭐ Rating: **{item.get('rating', '-')}**  
                ---
                """)
        
        elif isinstance(agent_result, str):  # If plain string
            st.markdown(agent_result)

        else:
            st.error("Error: Could not retrieve restaurant data.")
            st.json(result_json)

        # ------------------------------------------------------------

    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to the FastAPI server. Make sure it's running on http://127.0.0.1:8000.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Puraane 'if result.get("success")' block ko hata diya gaya hai.



