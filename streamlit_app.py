import streamlit as st
import requests

st.title("DeepSeek AI Search")

query = st.text_input("Enter your query:")
if query:
    response = requests.post("http://127.0.0.1:5000/search", json={"query": query})
    results = response.json()
    for result in results:
        st.write(result)