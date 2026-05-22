"""
This file tests the feature extraction part of PhishLLM.

I kept a print-based test here so I can manually see what features are being
detected, and I also added a simple pytest test for basic checking.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email
from feature_extract import extract_features


def test_feature_extraction_detects_phishing_indicators():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    parsed_email = parse_email(sample_email)
    features = extract_features(parsed_email)

    assert features["has_links"] is True
    assert features["has_urgency"] is True
    assert features["num_suspicious_keywords"] > 0


def run_test():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
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