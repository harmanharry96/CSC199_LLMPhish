"""
This file handles the rule-based feature extraction for PhishLLM.

I used this file to look for common phishing signs like suspicious words,
urgency language, links, and email addresses before sending the email
to the scoring engine.
"""

# These lists are simple rule-based indicators I used for the prototype.
# I updated them during testing when I noticed false positives and false negatives.
SUSPICIOUS_KEYWORDS = [
    "verify",
    "password",
    "passwords",
    "suspended",
    "click",
    "login",
    "confirm",
    "update",
    "secure",
    "validate",
    "payment",
    "invoice",
    "access",
    "credential",
    "credentials",
    "limited access",
    "security alert",
    "unauthorized",
    "reset",
    "unusual activity",
    "technical issue",
    "help desk",
    "remote access",
    "account locked",
    "account suspended",
]

URGENCY_WORDS = [
    "urgent",
    "immediately",
    "asap",
    "right now",
    "action required",
    "final notice",
    "within 24 hours",
    "last warning",
    "account closure",
]


def extract_features(parsed_email):
    body = (parsed_email.get("body") or "").lower()
    subject = (parsed_email.get("subject") or "").lower()
    full_text = f"{subject} {body}".strip()

    suspicious_keywords_found = find_keywords(full_text, SUSPICIOUS_KEYWORDS)
    urgency_words_found = find_keywords(full_text, URGENCY_WORDS)
    has_links = len(parsed_email.get("links", [])) > 0
    has_email_addresses = len(parsed_email.get("email_addresses", [])) > 0

    return {
        "suspicious_keywords_found": suspicious_keywords_found,
        "num_suspicious_keywords": len(suspicious_keywords_found),
        "urgency_words_found": urgency_words_found,
        "has_urgency": len(urgency_words_found) > 0,
        "has_links": has_links,
        "num_links": len(parsed_email.get("links", [])),
        "has_email_addresses": has_email_addresses,
        "num_email_addresses": len(parsed_email.get("email_addresses", []))
    }


def find_keywords(text, keyword_list):
    found = []

    for keyword in keyword_list:
        if keyword in text:
            found.append(keyword)

    return found