import streamlit as st
import tempfile
import os
from rag import ingest_pdf, query

st.title("RAG Assistant")

st.sidebar.title("Defense Controls")
enable_ifc = st.sidebar.toggle("Information Flow Control (Biba)", value=True)
enable_sanitization = st.sidebar.toggle("Input Sanitization", value=True)
enable_output_filter = st.sidebar.toggle("Output Filtering", value=True)

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

st.header("2. Ask a Question")
question = st.text_input("Enter your question")

if question:
    with st.spinner("Thinking..."):
        response, flagged = query(question, enable_ifc=enable_ifc, enable_sanitization=enable_sanitization, enable_output_filter=enable_output_filter)
    if flagged:
        st.warning(response)
    else:
        st.write(response)