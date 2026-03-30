SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "passwords",
    "suspended",
    "click",
    "bank",
    "account",
]

URGENCY_WORDS = [
    "urgent",
    "immediately",
    "asap",
    "right now",
    "important",
    "today",
    "action required",
    "final notice",
]

def extract_features(parsed_email):
    """
    Extract basic phishing-related features from the parsed email.
    """
    body = (parsed_email.get("body") or "").lower()
    subject = (parsed_email.get("subject") or  "").lower()
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

def find_keywords(text,keyword_list):
    """
    Return a list of keywords found in the text.
    """
    found = []
    for keyword in keyword_list:
        if keyword in text:
            found.append(keyword)           
    return found    
