import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email
from feature_extract import extract_features
from llm_check import analyze_with_llm
from scorer import score_email

def run_test():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    parsed = parse_email(sample_email)
    features = extract_features(parsed)
    llm_result = analyze_with_llm(parsed)
    score_result = score_email(features, llm_result)
    
    print("\n--- PARSED EMAIL ---")
    print(parsed)

    print("\n--- FEATURES ---")
    print(features)

    print("\n--- LLM RESULT ---")
    print(llm_result)

    print("\n--- FINAL SCORE RESULT ---")
    print(score_result)

if __name__ == "__main__":
    run_test()

