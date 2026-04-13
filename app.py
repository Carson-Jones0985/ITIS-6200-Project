import streamlit as st
import tempfile
import os
from rag import ingest_pdf, query

st.title("RAG Assistant")

# --- PDF Upload ---
st.header("1. Upload a Document")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Ingesting document..."):
        count = ingest_pdf(tmp_path)
    
    os.unlink(tmp_path)
    st.success(f"Ingested {count} chunks from {uploaded_file.name}")

# --- Question Answering ---
st.header("2. Ask a Question")
question = st.text_input("Enter your question")

if question:
    with st.spinner("Thinking..."):
        answer = query(question)
    st.write(answer)