# PDF Study Assistant Agent

This project is a Streamlit web application that acts as a study assistant. Users can upload a PDF document, and the application will generate a summary or a multiple-choice quiz based on the document's content.

## Features

*   **PDF Text Extraction:** Extracts text from uploaded PDF files.
*   **Summarization:** Generates a bulleted summary of the PDF content.
*   **Quiz Generation:** Creates multiple-choice quizzes from the PDF content.
*   **Interactive UI:** A user-friendly web interface built with Streamlit.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jawad-M-Mirza/AI-Driven-Development_30-Day-Challenge.git
    ```
2. **Navigate to the project directory:**
    ```bash
    cd Task_04/study-assistant
    ```
3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up environment variables:**
    - Create a `.env` file in the root of the project.
    - Add your Gemini API key to the `.env` file:
      ```
      GEMINI_API_KEY="YOUR_API_KEY"
      ```
5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

## Dependencies

The main dependencies of the project are:

*   [Streamlit](https://streamlit.io/): For creating the web application.
*   [pypdf](https://pypi.org/project/pypdf/): For extracting text from PDF files.
*   [openai-agents](https://pypi.org/project/openai-agents/): For interacting with the Gemini language model.
*   [python-dotenv](https://pypi.org/project/python-dotenv/): For managing environment variables.


## Configuration

The application requires a Gemini API key to be set as an environment variable. You can get your API key from [Google AI Studio](https://aistudio.google.com/).

Create a `.env` file in the project's root directory and add the following line:

```
GEMINI_API_KEY="your_gemini_api_key"
```
