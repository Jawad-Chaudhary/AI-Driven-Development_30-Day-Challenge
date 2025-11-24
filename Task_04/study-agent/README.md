# Study Notes Summarizer & Quiz Generator Agent

This project is an intelligent educational aide built with Streamlit and the `openai-agents` SDK. It processes PDF documents to create summaries and quizzes using the Google Gemini model.

## Features

-   **PDF Upload:** Upload PDF files directly through the Streamlit interface.
-   **Text Extraction:** Extracts text content from uploaded PDF documents.
-   **Notes Summarization:** Generates a concise, meaningful summary of the PDF content using bullet points and headers.
-   **Quiz Generation:** Creates a 5 Multiple Choice Question (MCQ) quiz based strictly on the provided PDF text, with answers at the end.

## Technology Stack

-   **Frontend:** Streamlit
-   **Backend Logic:** `openai-agents` SDK (for LLM orchestration), `pypdf` (for PDF text extraction)
-   **LLM:** Google Gemini (`gemini-2.0-flash` model via OpenAI Agents SDK)
-   **Dependency Management:** `uv`
-   **Environment Variables:** `python-dotenv`

## Setup and Installation

Follow these steps to get the application up and running on your local machine.

### 1. Clone the Repository

```bash
git clone <repository_url>
cd study-agent
```

### 2. Environment Setup

This project uses `uv` for dependency management. If you don't have `uv` installed, you can install it using pip:

```bash
pip install uv
```

### 3. Install Dependencies

Install the required Python packages:

```bash
uv pip install
```

### 4. Configure API Key

Create a `.env` file in the root directory of the project:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual Google Gemini API key. You can obtain one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Run the Application

Once the setup is complete, you can run the Streamlit application:

```bash
streamlit run app.py
```

This will open the application in your web browser.

## Usage

1.  **Upload a PDF:** Use the "Upload a PDF file" section in the sidebar to upload your study material.
2.  **Summarize:** Click the "Summarize Document" button to generate a summary of the uploaded PDF.
3.  **Create Quiz:** Click the "Create Quiz" button to generate a multiple-choice quiz based on the PDF content.

The generated summary and quiz will be displayed in the main section of the application.

## Project Structure

```
.
├── .env                  # Environment variables (GEMINI_API_KEY)
├── utils.py              # PDF processing logic (PyPDF)
├── agent.py              # Agent configuration & prompt definitions
├── app.py                # Streamlit UI & State Management
├── pyproject.toml        # UV Config
├── README.md             # Project README
└── .gitignore            # Git ignore file
```
