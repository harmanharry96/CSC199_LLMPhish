"""
This file tests the LLM analysis part of PhishLLM.

I use the fallback option here so the test can still run even if Gemini
is slow or unavailable during testing.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email
from llm_check import analyze_with_llm


def test_llm_or_fallback_returns_result():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    parsed = parse_email(sample_email)
    result = analyze_with_llm(parsed, use_mock_fallback=True)

    assert result is not None
    assert "Risk Level:" in result
    assert "Final Verdict:" in result


def run_test():
    sample_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com
"""

    parsed = parse_email(sample_email)
    result = analyze_with_llm(parsed, use_mock_fallback=True)

    print("\n--- PARSED EMAIL ---")
    print(parsed)

    print("\n--- LLM/FALLBACK ANALYSIS RESULT ---")
    print(result)


if __name__ == "__main__":
    run_test()