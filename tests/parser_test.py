import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from email_parser import parse_email


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