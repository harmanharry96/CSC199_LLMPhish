import csv
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from email_parser import parse_email
from feature_extract import extract_features
from llm_check import analyze_with_llm
from scorer import score_email

def load_dataset(input_csv):
    samples = []
    with open(input_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            samples.append(row)
    return samples

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
        "false_negatives": false_negatives

    }

def save_csv(rows, output_file):
    if not rows:
        return 
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def run_testing_framework(input_csv, results_csv, error_csv):
    dataset = load_dataset(input_csv)
    results = []

    for i, row in enumerate(dataset, start=1):
        subject = row.get("subject", "")
        body = row.get("body", "")
        actual_label = row.get("label", "0")

        raw_email = {
            "subject": subject,
            "body": body
        }

        try:
            parsed_email = parse_email(raw_email)
            features = extract_features(parsed_email)
            llm_result = analyze_with_llm(parsed_email)
            decision = score_email(features, llm_result)

            predicted_label = int(decision["label"])
            reason = decision.get("reason", "")

            result_row = {
                "id": row.get("id", i),
                "subject": subject,
                "body": body,
                "actual_label": actual_label,
                "predicted_label": predicted_label,
                "match": actual_label == predicted_label,
                "decision_reason": reason,
                "features": str(features),
                "llm_result": str(llm_result)

            }

            results.append(result_row)
            print(f"Processed email {i}/{len(dataset)}")

        except Exception as e:
            print(f"Error processing email {i}: {e}")
            results.append({
                "id": row.get("id", i),
                "subject": subject,
                "body": body,
                "actual_label": actual_label,
                "predicted_label": -1,
                "match": False,
                "decision_reason": f"Error: {str(e)}",
                "features": "",
                "llm_result": ""

            })

    valid_results = [r for r in results if r["predicted_label"] in [0, 1]]
    error_rows = [r for r in valid_results if not r["match"]]

    save_csv(valid_results, results_csv)
    save_csv(error_rows, error_csv)

    metrics = calculate_metrics(valid_results)

    print("\n--- Testing Summary ---")
    print(f"Total Samples: {metrics['total_samples']}")
    print(f"Correct Predictions: {metrics['correct_predictions']}")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"True Positives: {metrics['true_positives']}")
    print(f"True Negatives: {metrics['true_negatives']}")
    print(f"False Positives: {metrics['false_positives']}")
    print(f"False Negatives: {metrics['false_negatives']}")

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    run_testing_framework(
        input_csv="data/splits/test.csv",
        results_csv="results/test_results.csv",
        error_csv="results/test_errors.csv"
    )
