from gemini import get_gemini_client


def analyze_with_llm(parsed_email):
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
Short Reason: (1-2 sentence explanation)
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text_output = getattr(response, "text", None)

        if text_output and text_output.strip():
            return text_output.strip()

        return "LLM returned no usable output."

    except Exception:
        return "LLM Analysis Unavailable (Gemini API busy or temporarily unreachable)."