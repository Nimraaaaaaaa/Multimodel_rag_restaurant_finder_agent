import streamlit as st
import requests

st.title("Restaurant Finder")

uploaded_file = st.file_uploader("Upload dish image", type=["jpg","png"])
text_input = st.text_input("Enter your preferences")

if st.button("Find Restaurants") and uploaded_file and text_input:
    path = f"temp_{uploaded_file.name}"
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    files = {"file": open(path,"rb")}
    data = {"text": text_input}
    response = requests.post("http://127.0.0.1:8000/recommend", files=files, data=data)
    st.write(response.json()['recommendations'])
