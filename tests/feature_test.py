import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email
from feature_extract import extract_features

def run_test():
    sample_email = """
Subject: Bank Account Details for Member

Bank Account Details for Member

Member, please go over your details and click ahead to discover your new checking account!

"""

    parsed_email = parse_email(sample_email)
    features = extract_features(parsed_email)

    print("\n--- PARSED EMAIL ---")
    print(parsed_email)

    print("\n--- EXTRACTED FEATURES ---")
    for key, value in features.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    run_test()
