import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email
from llm_check import analyze_with_llm


def run_test():
    print("llm_test.py started")

    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    parsed = parse_email(sample_email)

    print("\n--- PARSED EMAIL ---")
    print(parsed)

    result = analyze_with_llm(parsed)

    print("\n--- LLM ANALYSIS RESULT ---")
    print(repr(result))


if __name__ == "__main__":
    run_test()