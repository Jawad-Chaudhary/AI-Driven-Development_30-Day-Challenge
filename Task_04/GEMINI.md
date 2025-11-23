# Role: Senior Python AI Engineer
**Objective**: Build a "PDF Study Assistant Agent" using Streamlit and the openagents SDK.

## 1. Project Overview
The goal is to develop a functional educational tool that processes PDF documents to aid student learning.
  - **UI**: Streamlit (Clean, interactive web interface).
  - **Core Logic**: openagents SDK (Agent orchestration).
  - **Model**: Google Gemini (via OpenAI-compatible endpoint).
  - **Tools**: pypdf (Text extraction) and context7 (Documentation retrieval during build).
  - **Memory:** Local JSON file storage (accessed via function calling).

## 2. Critical Technical Constraints
**You must adhere to the following strict configuration rules:**

  1. **Knowledge Acquisition Protocol (CRITICAL):**
    - **Before coding**, you **MUST** use the **Context7 MCP tool** to read the latest official documentation for:
      - openagents SDK (Focus on agent initialization and message handling).
      - streamlit (Focus on st.file_uploader and st.session_state).
      - pypdf (Focus on PdfReader).
    - Do not rely on internal training data for library syntax; libraries update frequently. Verify via Context7.

  2. **Zero-Bloat Protocol:**
    - Focus strictly on the requirements: PDF Summarization and Quiz Generation.
    - Do not add authentication, complex databases, or css-styling unless necessary for basic readability.
  
  3. **API Configuration:**
    - **Base URL:** https://generativelanguage.googleapis.com/v1beta/openai/
    - **API Key:** Load GEMINI_API_KEY from environment variables.
    - **Model:** Use gemini-2.0-flash (or equivalent available Gemini model).

  4. **Streamlit State Management:**
    - Streamlit reruns the script on every interaction. You must use st.session_state to persist the extracted PDF text and the agent's responses between the "Summarize" and "Quiz" button clicks.

## 3. Architecture & File Structure
.
├── .env                  # API Keys
├── utils.py              # PDF Extraction Logic
├── agent.py              # OpenAgents SDK Configuration
├── app.py                # Streamlit UI & State Management
└── pyproject.toml        # Dependencies (uv managed)

## 4. Implementation Steps

**Follow this exact logical flow.**

**Step 1: Documentation Retrieval (Context7)**

**Action**: Use Context7 to fetch and read documentation. Goal: Confirm the exact import syntax for openagents and how to pass the custom Gemini Base URL to it.

**Step 2: PDF Logic (utils.py)**
Create a helper function to handle the raw file processing.
  - **Function:** extract_text_from_pdf(file_object)
  - **Logic:** Use pypdf.PdfReader. Iterate through pages and concatenate text.
  - **Return:** A clean string of the full document text.

**Step 3: Agent Configuration (agent.py)**
Configure the AI logic using openagents.
  - **Setup:** Initialize the Agent with the Gemini-compatible OpenAI client.
  - **System Prompt:** Define the agent as an "Educational Assistant."
  - **Capabilities:**
    - Define a method/prompt for summarize(text): "Create a clean, bulleted summary of the provided text."
    - Define a method/prompt for generate_quiz(text): "Generate 5 Multiple Choice Questions based on the text. Format the output clearly with the question, options, and the correct answer hidden or at the bottom."

**Step 4: UI Integration (app.py)**

Build the interface.
  1. **Upload:** Use st.file_uploader (restrict to .pdf).
  2. **State:** Check if a file is uploaded. If yes, extract text once and store in st.session_state['pdf_text'].
  3. **Section A (Summarizer):**
    - Button: "Summarize Document".
    - Action: Call Agent summarize. Display result in a clean container (Markdown).
  4. **Section B (Quiz Generator):**
    - Button: "Create Quiz".
    - Action: Call Agent generate_quiz using the original st.session_state['pdf_text'].
    - Display result.

**Step 5: Dependency Management**
  - Use uv to initialize the project.
  - Ensure openagents, streamlit, pypdf, and python-dotenv are in pyproject.toml.

## 5. Testing Scenarios
  1. **Upload Flow:** Upload a generic PDF. Confirm no errors occur during extraction.
  2. **Summarization:** Click "Summarize". Result should be a concise bulleted list, not a wall of text.
  3. **Quiz Logic:** Click "Create Quiz".
    - **Verification:** The quiz must be based on the PDF content, not general knowledge.
    - **Format:** Ensure options (A, B, C, D) are visible.

  4. **Persistence:** Upload a PDF -> Summarize -> Create Quiz. Ensure the text didn't vanish or require re-uploading between steps.