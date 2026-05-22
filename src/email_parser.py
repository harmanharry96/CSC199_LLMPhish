"""
This file handles basic email parsing for PhishLLM.

I kept this separate because the rest of the project needs the email
broken into useful parts first, like subject, body, links, and email addresses.
"""

import re


def parse_email(email_text):
    if not email_text:
        return {
            "subject": None,
            "body": "",
            "links": [],
            "email_addresses": []
        }

    cleaned_text = clean_email_text(email_text)
    subject = extract_subject(cleaned_text)
    links = extract_links(cleaned_text)
    email_addresses = extract_email_addresses(cleaned_text)

    body = cleaned_text
    if subject and cleaned_text.lower().startswith("subject:"):
        lines = cleaned_text.splitlines()
        body = "\n".join(lines[1:]).strip()

    return {
        "subject": subject,
        "body": body,
        "links": links,
        "email_addresses": email_addresses
    }


def clean_email_text(email_text):
    email_text = email_text.strip()
    email_text = re.sub(r"\r\n", "\n", email_text)
    email_text = re.sub(r"[ \t]+", " ", email_text)
    email_text = re.sub(r"\n{3,}", "\n\n", email_text)
    return email_text


def extract_links(email_text):
    url_pattern = r"(https?://[^\s]+|www\.[^\s]+)"
    links = re.findall(url_pattern, email_text)

    cleaned_links = []
    for link in links:
        cleaned_links.append(link.rstrip(".,);]}>\"'"))

    return cleaned_links


def extract_email_addresses(email_text):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    return re.findall(email_pattern, email_text)


def extract_subject(email_text):
    lines = email_text.splitlines()

    if lines and lines[0].lower().startswith("subject:"):
        return lines[0][len("Subject:"):].strip()

    return None