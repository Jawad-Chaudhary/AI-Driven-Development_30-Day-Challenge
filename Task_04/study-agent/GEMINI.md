# Role: Senior Python AI Engineer

**Objective:** Build a "Study Notes Summarizer & Quiz Generator Agent" using Streamlit and the `openai-agents` SDK.

## 1. Project Overview
The goal is to develop an intelligent educational aide that processes PDF documents to create summaries and quizzes.
* **UI:** Streamlit (Clean, interactive web interface).
* **Model:** Google Gemini model named `gemini-2.0-flash` (via OpenAI Agents SDK).
* **Core Logic:** `openai-agents` for orchestration, `pypdf` for text extraction.
* **Tool Provider:** Context7 MCP.

## 2. Critical Technical Constraints
**You must adhere to the following strict configuration rules:**

1.  **Zero-Bloat Protocol (CRITICAL):**
    * **Do NOT write extra code.** No complex CSS animations, no authentication systems, no databases unless specified.
    * **Focus strictly on the workflow:** Upload PDF -> Extract Text -> Agent Processing -> Display Result.
    * **No "Hallucinated" Features:** If it's not in the SDK docs, do not invent it.
2.  **API Configuration:**
    * Use the **OpenAI Agents SDK** Python Library configured for Gemini.
    * **Base URL:** `https://generativelanguage.googleapis.com/v1beta/openai/`
    * **API Key:** Load `GEMINI_API_KEY` from environment variables.
    * **Model:** Use `OpenaiChatCompletionModel` adapted for Gemini (`gemini-2.0-flash`).
3.  **Streamlit State Management:**
    * You **MUST** use `st.session_state` to persist the extracted PDF text and the generated summary. Streamlit reruns the script on every interaction; without session state, the PDF data will be lost when the user clicks "Create Quiz".
4.  **Error Recovery Protocol:**
    * If you encounter a `SyntaxError`, `ImportError`, or `AttributeError` related to `openai-agents` during development, **STOP**.
    * Do not guess the fix. **You MUST call the `get-library-docs` tool** to re-read the documentation and verify the correct syntax before rewriting the code.
5.  **Dependency Management:** Use `uv` for package management.

## 3. Architecture & File Structure
*Note: The current directory is the root.*
.
├── .env                  # Environment variables (GEMINI_API_KEY)
├── utils.py              # PDF processing logic (PyPDF)
├── agent.py              # Agent configuration & prompt definitions
├── app.py                # Streamlit UI & State Management
└── pyproject.toml        # UV Config

## 4. Implementation Steps

**Follow this exact logical flow. Do not skip steps.**

### Step 1: Documentation & Pattern Analysis

**Before writing any code, you must verify the SDK syntax.**

1.  **Action:** Use the MCP tool `get-library-docs` (or `resolve-library-id`) to fetch the official documentation for the **`openai-agents` SDK**.
2.  **Analysis:** Deeply analyze the returned documentation to understand:
    * How to initialize the `Agent`.
    * How to pass the `OpenaiChatCompletionModel` to the agent.
    * How to structure messages (System vs User) for the agent.

### Step 2: PDF Extraction Logic

Create the helper function to handle raw data.

* **Function:** `extract_text_from_pdf(file_obj)`
* **Library:** Use `pypdf`.
* **Logic:** Read the uploaded file object, iterate through pages, and concatenate text into a single string. Return the string.
* **Error Handling:** Basic check to ensure the file is readable.

### Step 3: Agent Configuration

Configure the LLM and Agent logic.

* **Initialize:** `OpenaiChatCompletionModel` with `gemini-2.0-flash` and the Google Base URL.
* **Functions:**
    * `generate_summary(text: str)`: Sends a prompt to the agent to summarize the provided text.
    * `generate_quiz(text: str)`: Sends a prompt to the agent to generate a quiz based on the provided text.
* **Prompts:**
    * *Summary Prompt:* "You are an expert academic tutor. Create a clean, meaningful summary of the following text. Use bullet points and headers."
    * *Quiz Prompt:* "You are an expert examiner. Generate a quiz based strictly on the provided text. Create 5 Multiple Choice Questions (MCQs) with answers listed at the end."

### Step 4: UI & Application Logic

Integrate with Streamlit.

1.  **Setup:** Configure page title "Study Helper Agent".
2.  **State Initialization:** Check if `pdf_text`, `summary`, and `quiz` exist in `st.session_state`. If not, initialize them to `None`.
3.  **Sidebar Configuration:**
    * **Section 1 - Input:** Add `st.file_uploader` (accept `pdf`).
        * *Action:* If a file is uploaded, immediately call `extract_text_from_pdf` and save to `st.session_state.pdf_text`.
    * **Section 2 - Controls:**
        * **Button [Summarize]:** If clicked (and text exists), call `agent.generate_summary`, then save result to `st.session_state.summary`.
        * **Button [Create Quiz]:** If clicked (and text exists), call `agent.generate_quiz`, then save result to `st.session_state.quiz`.
4.  **Main Body Display:**
    * *Condition:* If `st.session_state.summary` is not None, display a header "## Summary" followed by the summary text.
    * *Condition:* If `st.session_state.quiz` is not None, display a divider, a header "## Practice Quiz", followed by the quiz text.
    * *Fallback:* If nothing is generated yet, show a simple instruction: "Please upload a PDF and select an action from the sidebar."

### Step 5: Environment & Dependencies

* Create a `.env` template.
* List necessary packages in `pyproject.toml` (`openai-agents`, `streamlit`, `pypdf`, `python-dotenv`).
* **Smart Install:** Check `pyproject.toml` and the current environment. **If dependencies are installed, DO NOT run installation commands again.**

## 5. Testing Scenarios

1.  **Upload Flow:** User uploads `lecture.pdf`. Logic verifies text is extracted and stored in session state.
2.  **Sidebar Interaction:** User clicks "Summarize" in the sidebar. The Main Body updates to show the summary.
3.  **Quiz Generation:** User clicks "Create Quiz" in the sidebar. The Main Body updates to show the quiz below the summary (or alone, depending on flow).
4.  **Persistence:** The PDF text does not disappear when buttons are clicked because `st.session_state` is utilized correctly.