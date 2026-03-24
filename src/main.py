from gemini import get_gemini_client


def check_phishing():
    try:
        client = get_gemini_client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Analyze this email for phishing indicators: 'Your account has been suspended. Click here to verify immediately.'"
        )

        print("\n--- Analysis Result ---")
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_phishing()