from google import genai
import os

# Loads the .env file so os.getenv() can access it


# API key is pulled from the .env file, not hardcoded
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def check_phishing():
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Analyze this URL for potential phishing indicators: 'http://secure-login-wellsfargo.com'"
        )
        print("\n--- Analysis Result ---")
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_phishing()