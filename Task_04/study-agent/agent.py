import os
from openai import AsyncOpenAI
from agents import Agent, Runner
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

GOOGLE_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Initialize OpenAI Client adapted for Gemini
aclient = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=GOOGLE_BASE_URL,
)

# Initialize OpenaiChatCompletionModel
# This model will be used by the agent to interact with the Gemini API
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=aclient,
)

# Initialize the Agent
# We'll create a generic agent for now, and instruct it for specific tasks later
# via the function prompts.
study_agent = Agent(
    name="StudyHelper",
    model=gemini_model,
    # No specific instructions here, as instructions will be part of the function calls
)

async def generate_summary(text: str) -> str:
    """
    Sends a prompt to the agent to summarize the provided text.
    """
    summary_prompt = (
        "You are an expert academic tutor. Create a clean, meaningful summary of the following text. "
        "Use bullet points and headers."
    )
    result = await Runner.run(starting_agent=study_agent,input=f"{summary_prompt}\n\n{text}")
    return result.final_output

async def generate_quiz(text: str) -> str:
    """
    Sends a prompt to the agent to generate a quiz based on the provided text.
    """
    quiz_prompt = (
        "You are an expert examiner. Generate a quiz based strictly on the provided text. "
        "Create 5 Multiple Choice Questions (MCQs) with answers listed at the end."
    )
    result = await Runner.run(starting_agent=study_agent,input=f"{quiz_prompt}\n\n{text}")
    return result.final_output
