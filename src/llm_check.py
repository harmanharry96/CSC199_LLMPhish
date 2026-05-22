"""
This file handles the LLM part of PhishLLM.

It sends the parsed email to Gemini for analysis. I also added a fallback
method so the project can still return a result when Gemini is unavailable.
"""

from gemini import get_gemini_client


def analyze_with_llm(parsed_email, use_mock_fallback=True):
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
        client = get_gemini_client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text_output = getattr(response, "text", None)

        if text_output and text_output.strip():
            return text_output.strip()

        return fallback_llm_result(parsed_email) if use_mock_fallback else "LLM returned no usable output."

    except Exception:
        return fallback_llm_result(parsed_email) if use_mock_fallback else "LLM Analysis Unavailable."


def fallback_llm_result(parsed_email):
    subject = (parsed_email.get("subject") or "").lower()
    body = (parsed_email.get("body") or "").lower()
    text = f"{subject} {body}"

    links = parsed_email.get("links", [])

    credential_terms = [
        "verify",
        "login",
        "password",
        "credential",
        "credentials",
        "confirm",
        "reset",
        "validate",
    ]

    threat_terms = [
        "suspended",
        "locked",
        "unauthorized",
        "unusual activity",
        "account closure",
        "limited access",
    ]

    urgency_terms = [
        "urgent",
        "immediately",
        "action required",
        "within 24 hours",
        "final notice",
    ]

    tech_support_terms = [
        "technical issue",
        "help desk",
        "remote access",
        "security alert",
        "system error",
    ]

    credential_hits = sum(1 for term in credential_terms if term in text)
    threat_hits = sum(1 for term in threat_terms if term in text)
    urgency_hits = sum(1 for term in urgency_terms if term in text)
    tech_hits = sum(1 for term in tech_support_terms if term in text)

    has_link = len(links) > 0

    # I used combinations here because one keyword by itself was causing false positives.
    if (
        (has_link and credential_hits >= 1)
        or (urgency_hits >= 1 and credential_hits >= 1)
        or (threat_hits >= 1 and credential_hits >= 1)
        or (credential_hits + threat_hits + urgency_hits + tech_hits >= 3)
    ):
        return """Risk Level: High
Confidence Score: 70
Final Verdict: Phishing
Short Reason: Gemini was unavailable, so fallback analysis was used. Multiple phishing indicators were detected in combination."""

    # Medium risk catches weaker suspicious patterns without making everything high risk.
    if urgency_hits >= 1 and (
        "payment" in text
        or "access" in text
        or "account" in text
        or "update" in text
        or "click" in text
    ):
        return """Risk Level: Medium
Confidence Score: 55
Final Verdict: Phishing
Short Reason: Gemini was unavailable, so fallback analysis was used. Urgency language appeared with a suspicious account/payment/action-related term."""

    # This is for weaker signals that still look suspicious but are not strong enough for high risk.
    if (
        credential_hits >= 1
        or threat_hits >= 1
        or tech_hits >= 1
        or (has_link and urgency_hits >= 1)
    ):
        return """Risk Level: Medium
Confidence Score: 55
Final Verdict: Phishing
Short Reason: Gemini was unavailable, so fallback analysis was used. Some suspicious indicators were detected, but confidence is limited."""

    return """Risk Level: Low
Confidence Score: 50
Final Verdict: Legitimate
Short Reason: Gemini was unavailable, so fallback analysis was used. No strong phishing indicator combinations were detected."""