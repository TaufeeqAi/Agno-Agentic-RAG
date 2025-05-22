# streamlit_app.py
import streamlit as st
import requests

# Point this to your FastAPI server
API_URL = "http://localhost:8000/query"

st.set_page_config(page_title="Agentic RAG with CoT", layout="centered")
st.title("🤖 Agentic RAG Chat")

user_query = st.text_input("Enter your question:")

if st.button("Submit") and user_query:
    with st.spinner("Thinking....."):
        try:
            resp = requests.post(
                API_URL,
                json={"text": user_query},
                
            )
            resp.raise_for_status()
            data = resp.json()
            reasoning = data["reasoning"]
            answer = data["answer"]
            
            st.subheader("🧠 Chain of Thoughts ")
            
            with st.expander("🔗 Show reasoning Steps 🪄"):
                for i, step in enumerate(reasoning, 1):
                    st.markdown(f"**Step {i}:** {step}")
            st.subheader("Answer")
            st.markdown(answer)

        except requests.exceptions.RequestException as err:
            st.error(f"Error: {err}")
