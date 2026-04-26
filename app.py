import streamlit as st
import tempfile
import os
from rag import ingest_pdf, query

if "log" not in st.session_state:
    st.session_state.log = []

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

# if question:
#     with st.spinner("Thinking..."):
#         response, flagged = query(question, enable_ifc=enable_ifc, enable_sanitization=enable_sanitization, enable_output_filter=enable_output_filter)
#     if flagged:
#         st.warning(response)
#     else:
#         st.write(response)

if question:
    with st.spinner("Thinking..."):
        response, flagged, details = query(
            question,
            enable_ifc=enable_ifc,
            enable_sanitization=enable_sanitization,
            enable_output_filter=enable_output_filter
        )

    if flagged:
        st.warning(response)
        st.session_state.log.append(f"BLOCKED: {response}")
    else:
        st.write(response)
        st.session_state.log.append(f"ALLOWED: {question}")

    # Defense details expander
    with st.expander(" Defense Details"):
        if enable_sanitization:
            st.subheader("Input Sanitization")
            if details["flagged_chunks"]:
                st.error(f"{len(details['flagged_chunks'])} chunk(s) flagged and cleaned:")
                for chunk in details["flagged_chunks"]:
                    st.code(chunk)
            else:
                st.success("No injection phrases detected in chunks.")

        if enable_ifc:
            st.subheader("Information Flow Control (Biba)")
            if details["ifc_violations"]:
                st.error("Violations detected:")
                for v in details["ifc_violations"]:
                    st.code(v)
            else:
                st.success("No Biba integrity violations detected.")

        if enable_output_filter:
            st.subheader("Output Filter")
            if details["output_warning"]:
                st.error(details["output_warning"])
            else:
                st.success("Response passed output filter.")