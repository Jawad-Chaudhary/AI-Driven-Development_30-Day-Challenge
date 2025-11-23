import json
import os
from agents import Agent, Runner, set_default_openai_key, set_default_openai_api, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig # type: ignore
from dotenv import load_dotenv
import asyncio

load_dotenv()


MODEL_NAME = "gemini-2.0-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model = MODEL_NAME,
    openai_client = external_client,
)

config = RunConfig(
    model_provider = external_client, # type: ignore
    model = model,
)

# Initialize the Agent with the Gemini model
agent = Agent(
    name="PDF Study Assistant",
    instructions="You are an Educational Assistant. Your goal is to help students learn from PDF documents.",
    model = model
)

async def summarize(text):
    """
    Creates a clean, bulleted summary of the provided text.
    """
    prompt = (
        "Create a concise, easy-to-read, bulleted summary of the following text. "
        "Focus on the key points and main ideas. Avoid jargon and unnecessary details.\n\n"
        f"Text:\n{text}"
    )
    result = await Runner.run(agent, prompt)
    return result.final_output

async def generate_quiz(text, num_questions=5):
    """
    Generates a specified number of Multiple Choice Questions based on the text.
    Returns a list of dictionaries, each containing 'question', 'options', and 'answer'.
    """
    # For quiz, structured output is also a good idea, but I'll keep it as is for now to focus on flashcards.
    prompt = (
        f"Generate {num_questions} Multiple Choice Questions based on the following text. "
        "For each question, provide 4 options (A, B, C, D) and specify the correct answer. "
        "Return the output as a JSON array of objects, where each object has 'question', 'options' (an array of strings), and 'answer' fields. "
        "Example: [{'question': '...', 'options': ['A. ...', 'B. ...', 'C. ...', 'D. ...'], 'answer': 'A'}, ...]\n\n"
        f"Text:\n{text}"
    )
    result = await Runner.run(agent, prompt)
    
    try:
        quiz_data = json.loads(result.final_output)
        if isinstance(quiz_data, list) and all(isinstance(item, dict) for item in quiz_data):
            return quiz_data
        else:
            return []
    except json.JSONDecodeError:
        return []