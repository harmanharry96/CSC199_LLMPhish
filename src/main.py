from google import genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GEMINI_API_KEY")  # Get API key from environment variable  
client = genai.Client(api_key=API_KEY)

def analyze_url(url):
    prompt = f"""
You are a cybersecurity assistant specialized in phishing detection.

Analyze the following URL for possible phishing indicators:

URL: {url}

Check for:
- suspicious domain names
- brand impersonation
- typosquatting
- unusual subdomains
- misleading words like login, secure, verify

Return:
Risk Level:
Reasons:
Final Verdict:
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print(response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    url = input("Enter URL: ")
    analyze_url(url)