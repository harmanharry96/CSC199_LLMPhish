"""
This file tests the final scoring part of PhishLLM.

I use the fallback option here so the scoring test can run even when
Gemini is unavailable or slow.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email
from feature_extract import extract_features
from llm_check import analyze_with_llm
from scorer import score_email


def test_score_email_returns_final_result():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    parsed = parse_email(sample_email)
    features = extract_features(parsed)
    llm_result = analyze_with_llm(parsed, use_mock_fallback=True)
    score_result = score_email(features, llm_result)

    assert "final_score" in score_result
    assert "risk_level" in score_result
    assert "final_verdict" in score_result
    assert score_result["final_verdict"] in ["Phishing", "Suspicious", "Legitimate"]


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
    llm_result = analyze_with_llm(parsed, use_mock_fallback=True)
    score_result = score_email(features, llm_result)

    print("\n--- PARSED EMAIL ---")
    print(parsed)

    print("\n--- FEATURES ---")
    print(features)

    print("\n--- LLM/FALLBACK RESULT ---")
    print(llm_result)

    print("\n--- FINAL SCORE RESULT ---")
    print(score_result)


if __name__ == "__main__":
    run_test()