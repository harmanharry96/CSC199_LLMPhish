"""
This file parses emails from the Enron dataset.

I used Enron emails as legitimate examples so the project could test
phishing emails against normal email communication.
"""

import os
import pandas as pd


def extract_email_body(file_path):
    try:
        with open(file_path, "r", encoding="latin-1") as f:
            content = f.read()

        # Enron files usually have headers first, then the email body.
        parts = content.split("\n\n", 1)

        if len(parts) > 1:
            body = parts[1].strip()
        else:
            body = content.strip()

        return body

    except Exception:
        return ""


def parse_enron_datasets(base_path, max_emails=5000):
    data = []
    count = 0

    print("Parsing Enron emails...")

    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            body = extract_email_body(file_path)

            if body and len(body) > 20:
                data.append({
                    "text": body,
                    "label": 0,
                    "source": "enron",
                    "phishing_type": "legitimate"
                })

                count += 1

                if count % 500 == 0:
                    print(f"Parsed {count} emails...")

            if count >= max_emails:
                print("Reached limit.")
                return pd.DataFrame(data)

    return pd.DataFrame(data)