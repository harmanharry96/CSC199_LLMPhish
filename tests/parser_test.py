"""
This file tests the email parser.

I kept a manual print test here so I can see the parsed output,
and I also added a simple pytest test for basic checking.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email


def test_parser_extracts_subject_body_and_links():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    result = parse_email(sample_email)

    assert result["subject"] == "Urgent Account Verification"
    assert "Your account has been suspended." in result["body"]
    assert "http://secure-login-bank.com" in result["links"]


def run_test():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    result = parse_email(sample_email)

    print("\n--- Parsed Email Output ---")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    run_test()