# PhishLLM

PhishLLM is my CSC199 research project. It is a prototype phishing email detection system that analyzes emails and predicts whether they are phishing or legitimate.

The project uses a hybrid approach:

1. Rule-based email feature extraction
2. Gemini LLM-based analysis
3. A scoring/decision engine
4. A testing framework that saves results and errors

This project is not meant to be a perfect production-level security tool. My main goal was to build and understand an end-to-end phishing detection pipeline, then test where it works well and where it still needs improvement.

---

## Project Overview

PhishLLM takes an email and runs it through several steps.

The system first parses the email into useful parts like the subject, body, and links. Then it checks for rule-based phishing indicators such as suspicious links, urgency language, credential-related words, and threat-based wording.

After that, the email can be analyzed by Gemini. The Gemini result is combined with the rule-based features inside the scoring engine to produce a final verdict.

If Gemini is unavailable, the project uses a fallback analysis so the program can still return a result instead of crashing.

---

## How the Pipeline Works

```text
Raw Email
   ↓
Email Parser
   ↓
Feature Extraction
   ↓
Gemini LLM Analysis / Fallback Analysis
   ↓
Scoring Engine
   ↓
Final Verdict
```

The final output includes:

- Risk level
- Final verdict
- Final score
- Short explanation from the LLM or fallback logic

---

## Project Structure

```text
CSC199_LLMPhish/
│
├── src/
│   ├── config.py
│   ├── email_parser.py
│   ├── feature_extract.py
│   ├── gemini.py
│   ├── llm_check.py
│   ├── scorer.py
│   ├── main.py
│   ├── main_data.py
│   ├── data_builder.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   └── enron_parser.py
│
├── tests/
│   ├── feature_test.py
│   ├── parser_test.py
│   ├── scorer_test.py
│   ├── llm_test.py
│   └── testing_framework.py
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── final/
│   └── splits/
│
├── results/
│   ├── test_results.csv
│   └── error_log.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Main Files

### `src/email_parser.py`

This file handles parsing the raw email text. It separates the email into subject, body, and links.

### `src/feature_extract.py`

This file handles the rule-based feature extraction. It looks for phishing indicators such as links, urgency words, credential-related terms, and suspicious wording.

### `src/gemini.py`

This file creates the Gemini client using the API key from the `.env` file.

### `src/llm_check.py`

This file sends the parsed email to Gemini for analysis. It also includes fallback logic so the project can still return a result if Gemini is unavailable.

### `src/scorer.py`

This file combines the rule-based features and the LLM/fallback result to calculate the final score and verdict.

### `src/main.py`

This file runs a simple demo of the full pipeline.

### `tests/testing_framework.py`

This file runs the detector on a labeled dataset and saves the output into CSV files.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/harmanharry96/CSC199_LLMPhish.git
cd CSC199_LLMPhish
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Gemini API key

Create a `.env` file in the main project folder.

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is ignored by Git because it contains the private API key.

---

## How to Run the Demo

Run this command from the main project folder:

```bash
python3 src/main.py
```

The demo prints each major step of the pipeline:

```text
Raw Email
Parsed Email Output
Feature Extraction Output
LLM Analysis Output
Decision Engine Output
Final Result
```

The demo includes example phishing and legitimate emails so the pipeline can be tested quickly.

---

## How to Run Unit Tests

Run:

```bash
pytest tests/
```

These tests check individual parts of the project, such as parsing, feature extraction, LLM handling, and scoring.

---

## How to Run the Testing Framework

Run:

```bash
python3 tests/testing_framework.py
```

The testing framework runs the detector on a labeled dataset and saves the results in the `results/` folder.

Output files:

```text
results/test_results.csv
results/error_log.csv
```

`test_results.csv` stores the prediction results.

`error_log.csv` stores cases where the prediction was wrong, which helped me understand false positives and false negatives.

---

## Final Testing Results

For the final 100-email test:

```text
Total Samples: 100
Correct Predictions: 75
Accuracy: 75.00%

True Positives: 23
True Negatives: 52
False Positives: 4
False Negatives: 21
```

Some tests used fallback analysis when Gemini was unavailable. This affected phishing detection, especially for phishing emails that did not have strong rule-based indicators such as links, credential words, or multiple suspicious keywords.

The false negatives mostly came from phishing emails that were more subtle and did not trigger enough rule-based indicators when Gemini was unavailable.

The false positives mostly came from legitimate emails that had links or words that looked suspicious to the rule-based system.

---

## Known Limitations

This project is a prototype, so it still has some limitations:

- The dataset is small compared to real-world phishing datasets.
- Gemini API availability affected some testing results.
- The fallback logic worked, but it was not always strong enough for subtle phishing emails.
- The project focuses mainly on email text and basic links, not full URL reputation analysis.

---

## Future Improvements

If I had more time, I would improve the project by adding:

- Better URL reputation analysis
- A larger and more realistic phishing dataset
- Stronger fallback logic when Gemini is unavailable
- Better scoring weights based on more testing
- More detailed error analysis
- A simple web interface for testing emails
- More phishing categories in the dataset

---

## What I Learned

This project helped me understand that phishing detection should not depend on only one method.

I learned how to parse email content, extract phishing indicators, use an LLM for security analysis, and combine both rule-based logic and LLM analysis inside a scoring system.

One important thing I learned is that AI or LLM output should not be the only final decision. In this project, I used both rule-based features and Gemini analysis so the final verdict was based on multiple signals.

I also learned how important testing is. By running the testing framework and checking the error log, I was able to see where the prototype worked well and where it struggled, especially with false positives and false negatives.

The final system is not perfect, but it shows a working prototype and helped me better understand both phishing detection and the challenges of using LLMs in cybersecurity projects.