
import streamlit as st
import asyncio
from utils import extract_text_from_pdf
from agent import generate_summary, generate_quiz

# 1. Setup: Configure page title
st.set_page_config(page_title="Study Helper Agent", layout="wide")
st.title("📚 Study Helper Agent")

# 2. State Initialization: Check if pdf_text, summary, and quiz exist in st.session_state.
# If not, initialize them to None.
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None

# 3. Sidebar Configuration
with st.sidebar:
    st.header("Input your Study Material")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Action: If a file is uploaded, immediately call extract_text_from_pdf
        # and save to st.session_state.pdf_text.
        if st.session_state.pdf_text is None or st.session_state.pdf_text != uploaded_file.name:
            # Only re-extract if a new file is uploaded or file content changed
            st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
            if "Error" in st.session_state.pdf_text:
                st.error(st.session_state.pdf_text)
                st.session_state.pdf_text = None
            else:
                st.success("PDF uploaded and text extracted!")
                # Clear previous summary/quiz if a new PDF is uploaded
                st.session_state.summary = None
                st.session_state.quiz = None

    st.header("Controls")
    if st.button("Summarize Document"):
        if st.session_state.pdf_text:
            with st.spinner("Generating summary..."):
                st.session_state.summary = asyncio.run(generate_summary(st.session_state.pdf_text))
                st.success("Summary generated!")
        else:
            st.warning("Please upload a PDF first to generate a summary.")

    if st.button("Create Quiz"):
        if st.session_state.pdf_text:
            with st.spinner("Generating quiz..."):
                st.session_state.quiz = asyncio.run(generate_quiz(st.session_state.pdf_text))
                st.success("Quiz generated!")
        else:
            st.warning("Please upload a PDF first to create a quiz.")

# 4. Main Body Display
if st.session_state.summary:
    st.markdown("## Summary")
    st.markdown(st.session_state.summary)

if st.session_state.quiz:
    st.markdown("---")
    st.markdown("## Practice Quiz")
    st.markdown(st.session_state.quiz)

# Fallback: If nothing is generated yet, show a simple instruction
if not st.session_state.summary and not st.session_state.quiz:
    st.info("Please upload a PDF and select an action from the sidebar.")

