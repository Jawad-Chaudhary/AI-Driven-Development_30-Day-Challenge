import streamlit as st
from utils import extract_text_from_pdf
from agent import summarize, generate_quiz
import asyncio

# Set the page title
st.title("PDF Study Assistant Agent")

# Create a file uploader
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Extract the text from the PDF and store it in the session state
    if "pdf_text" not in st.session_state:
        st.session_state["pdf_text"] = extract_text_from_pdf(uploaded_file)

    # Create a variable to control the main body view
    if "main_view" not in st.session_state:
        st.session_state["main_view"] = "initial"

    st.sidebar.title("Actions")
    if st.sidebar.button("Generate Summary"):
        st.session_state["main_view"] = "summary"
        # Summarize the text and store the result in the session state
        with st.spinner("Summarizing..."):
            st.session_state["summary"] = asyncio.run(summarize(st.session_state["pdf_text"]))
    
    # Prompt for number of quiz questions
    if "quiz_question_prompt" not in st.session_state:
        st.session_state["quiz_question_prompt"] = False
    
    if st.sidebar.button("Generate Quiz"):
        st.session_state["main_view"] = "quiz"
        st.session_state["quiz_question_prompt"] = True

    if st.session_state["quiz_question_prompt"]:
        num_questions = st.sidebar.number_input("Number of questions:", min_value=1, max_value=20, value=5)
        if st.sidebar.button("Create Quiz Now"):
            # Generate a quiz and store the result in the session state
            with st.spinner("Creating quiz..."):
                st.session_state["quiz"] = asyncio.run(generate_quiz(st.session_state["pdf_text"], num_questions))
            st.session_state["quiz_question_prompt"] = False # Hide the prompt after generation

    # Display content based on the main_view state
    if st.session_state["main_view"] == "summary" and "summary" in st.session_state:
        st.subheader("Summary")
        st.markdown(st.session_state["summary"])
    elif st.session_state["main_view"] == "quiz":
        st.subheader("Quiz")
        if "quiz" in st.session_state:
            quiz_data = st.session_state["quiz"]
            if isinstance(quiz_data, dict) and "error" in quiz_data:
                st.error(quiz_data["error"])
            elif isinstance(quiz_data, list) and quiz_data:
                if "show_answer" not in st.session_state or len(st.session_state["show_answer"]) != len(quiz_data):
                    st.session_state["show_answer"] = [False] * len(quiz_data)

                for i, qa in enumerate(quiz_data):
                    st.markdown(f"**Question {i+1}:** {qa['question']}")
                    for option in qa['options']:
                        st.write(option)
                    
                    button_key = f"show_answer_button_{i}"

                    def toggle_answer(index):
                        st.session_state["show_answer"][index] = not st.session_state["show_answer"][index]

                    st.button("Show Answer" if not st.session_state["show_answer"][i] else "Hide Answer", 
                              key=button_key, 
                              on_click=toggle_answer, 
                              args=(i,))
                    
                    if st.session_state["show_answer"][i]:
                        st.success(f"**Answer:** {qa['answer']}")
                    st.markdown("---") # Separator
            else:
                st.warning("Could not generate the quiz. Please try again or check the PDF content.")
    else:
        st.write("Upload a PDF and choose an action from the sidebar.")
