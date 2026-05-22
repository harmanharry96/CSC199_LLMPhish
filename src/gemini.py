"""
This file handles the Gemini API setup for PhishLLM.

I kept the API setup separate so the rest of the project can just call
get_gemini_client() without worrying about the API key setup.
"""

import os
from google import genai
from dotenv import load_dotenv


load_dotenv()  # Loads GEMINI_API_KEY from the local .env file.


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    return genai.Client(api_key=api_key)