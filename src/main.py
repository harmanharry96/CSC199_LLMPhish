from email_parser import parse_email
from feature_extract import extract_features
from llm_check import analyze_with_llm
from scorer import score_email


def pretty_print_dict(title, data):
    print(f"\n{title}")
    for key, value in data.items():
        print(f"{key}:")
        print(f"{value}\n")


def run_demo_case(case_name, sample_email):
    print("\n" + "=" * 60)
    print(f"DEMO CASE: {case_name}")
    print("=" * 60)

    print("\n1. Raw Email:")
    print(sample_email)

    print("\n2. Parsing Email...")
    parsed_email = parse_email(sample_email)
    pretty_print_dict("--- Parsed Email Output ---", parsed_email)

    print("\n3. Extracting Rule-Based Features...")
    features = extract_features(parsed_email)
    pretty_print_dict("--- Feature Extraction Output ---", features)

    print("\n4. Running LLM Analysis...")
    llm_result = analyze_with_llm(parsed_email, use_mock_fallback=True)
    print("\n--- LLM Analysis Output ---")
    print(llm_result)

    print("\n5. Running Decision Engine...")
    final_result = score_email(features, llm_result)
    pretty_print_dict("--- Decision Engine Output ---", final_result)

    print("\n=== Final Result ===")
    print(f"Risk Level: {final_result['risk_level']}")
    print(f"Final Verdict: {final_result['final_verdict']}")
    print(f"Final Score: {final_result['final_score']}")

    return final_result


def main():
    print("\n=== PhishLLM Demo Pipeline Started ===")

    phishing_email = """
Subject: Urgent Account Verification

Dear Customer,

Your account has been suspended.
Please verify immediately by clicking the link below:
http://secure-login-bank.com

Failure to act within 24 hours may result in permanent account closure.
"""

    legitimate_email = """
Subject: Team Meeting Reminder

Hi Team,

This is a reminder that we have our weekly project meeting tomorrow at 2 PM in Conference Room B.

Please review the agenda before attending.

Best,
Operations Manager
"""

    phishing_result = run_demo_case("Phishing Email Example", phishing_email)
    legitimate_result = run_demo_case("Legitimate Email Example", legitimate_email)

    print("\n" + "=" * 60)
    print("DEMO SUMMARY")
    print("=" * 60)
    print(f"Phishing Example Verdict: {phishing_result['final_verdict']} | Score: {phishing_result['final_score']}")
    print(f"Legitimate Example Verdict: {legitimate_result['final_verdict']} | Score: {legitimate_result['final_score']}")

    print("\n=== Demo Completed ===")


if __name__ == "__main__":
    main()