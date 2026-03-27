from gemini import get_gemini_client


def analyze_with_llm(parsed_email):
    print("Inside analyze_with_llm()")

    client = get_gemini_client()

    prompt = f"""
You are a cybersecurity assistant specialized in phishing detection.

Analyze the following email and determine if it is phishing.

Subject: {parsed_email.get("subject")}
Body: {parsed_email.get("body")}

Check for:
- Urgency or pressure tactics
- Suspicious links
- Requests for sensitive/classified information
- Impersonation
- Unusual tone or grammar

Return your response in this format:

Risk Level: (Low / Medium / High)
Confidence Score: (0-100)
Final Verdict: (Phishing / Legitimate)
"""

    try:
        print("Sending request to Gemini...")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("Response received from Gemini")

        text_output = getattr(response, "text", None)

        if text_output and text_output.strip():
            return text_output.strip()

        candidates = getattr(response, "candidates", None)
        if candidates:
            return str(candidates)

        return "No usable output returned by Gemini."

    except Exception as e:
        return f"Error: {e}"