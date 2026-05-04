import csv
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from email_parser import parse_email
from feature_extract import extract_features
from llm_check import analyze_with_llm
from scorer import score_email


MAX_SAMPLES = 10  # Starting small for testing


def load_dataset(input_csv, max_samples=None):
    samples = []

    with open(input_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for i, row in enumerate(reader):
            if max_samples is not None and i >= max_samples:
                break
            samples.append(row)

    return samples


def verdict_to_label(final_verdict):
    """
    Convert final verdict into numeric label.
    1 = phishing/suspicious
    0 = legitimate
    """
    if final_verdict in ["Phishing", "Suspicious"]:
        return 1
    return 0


def calculate_metrics(results):
    total = len(results)
    correct = 0
    false_positives = 0
    false_negatives = 0
    true_positives = 0
    true_negatives = 0

    for row in results:
        actual = int(row["actual_label"])
        predicted = int(row["predicted_label"])

        if actual == predicted:
            correct += 1

        if actual == 0 and predicted == 1:
            false_positives += 1

        if actual == 1 and predicted == 0:
            false_negatives += 1

        if actual == 1 and predicted == 1:
            true_positives += 1

        if actual == 0 and predicted == 0:
            true_negatives += 1

    accuracy = correct / total if total > 0 else 0

    return {
        "total_samples": total,
        "correct_predictions": correct,
        "accuracy": accuracy,
        "true_positives": true_positives,
        "true_negatives": true_negatives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


def save_csv(rows, output_file):
    if not rows:
        return

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def run_testing_framework(input_csv, results_csv, error_csv, max_samples=10):
    dataset = load_dataset(input_csv, max_samples=max_samples)
    results = []

    print("\n=== PhishLLM Testing Framework Started ===")
    print(f"Loaded {len(dataset)} sample emails.\n")

    for i, row in enumerate(dataset, start=1):
        raw_email = row.get("text", "")
        actual_label = int(row.get("label", 0))
        source = row.get("source", "unknown")
        phishing_type = row.get("phishing_type", "unknown")

        try:
            print(f"Processing email {i}/{len(dataset)}...")

            parsed_email = parse_email(raw_email)
            features = extract_features(parsed_email)
            llm_result = analyze_with_llm(parsed_email)
            decision = score_email(features, llm_result)

            final_verdict = decision["final_verdict"]
            predicted_label = verdict_to_label(final_verdict)

            result_row = {
                "id": i,
                "actual_label": actual_label,
                "predicted_label": predicted_label,
                "match": actual_label == predicted_label,
                "final_verdict": final_verdict,
                "risk_level": decision["risk_level"],
                "feature_score": decision["feature_score"],
                "llm_score": decision["llm_score"],
                "final_score": decision["final_score"],
                "source": source,
                "phishing_type": phishing_type,
                "subject": parsed_email.get("subject"),
                "links": parsed_email.get("links"),
                "features": str(features),
                "llm_result": str(llm_result),
            }

            results.append(result_row)

        except Exception as e:
            print(f"Error processing email {i}: {e}")

            results.append({
                "id": i,
                "actual_label": actual_label,
                "predicted_label": -1,
                "match": False,
                "final_verdict": "Error",
                "risk_level": "Error",
                "feature_score": 0,
                "llm_score": 0,
                "final_score": 0,
                "source": source,
                "phishing_type": phishing_type,
                "subject": "",
                "links": "",
                "features": "",
                "llm_result": f"Error: {str(e)}",
            })

    valid_results = [r for r in results if r["predicted_label"] in [0, 1]]
    error_rows = [r for r in valid_results if not r["match"]]

    save_csv(valid_results, results_csv)
    save_csv(error_rows, error_csv)

    metrics = calculate_metrics(valid_results)

    print("\n=== Testing Summary ===")
    print(f"Total Samples: {metrics['total_samples']}")
    print(f"Correct Predictions: {metrics['correct_predictions']}")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"True Positives: {metrics['true_positives']}")
    print(f"True Negatives: {metrics['true_negatives']}")
    print(f"False Positives: {metrics['false_positives']}")
    print(f"False Negatives: {metrics['false_negatives']}")

    print("\nResults saved to:")
    print(results_csv)
    print(error_csv)

    print("\n=== Testing Framework Completed ===")


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    run_testing_framework(
        input_csv="data/final/dataset_v2.csv",
        results_csv="results/test_results.csv",
        error_csv="results/error_log.csv",
        max_samples=MAX_SAMPLES,
    )