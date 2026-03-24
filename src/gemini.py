import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  # Loaded the environment variables from .env.

def get_gemini_client():
    """
    Creates and returns a Gemini API client using the API key from environment variables.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    return genai.Client(api_key=api_key)


