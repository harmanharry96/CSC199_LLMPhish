import re
import pandas as pd

def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""
    
    text = str(text)
    text = re.sub(r"<[^>]+>", " ", text)  # Remove HTML tags
    text = re.sub(r"\s+", " ", text)  # Replace multiple whitespace with
    text = text.strip()
    return text

def standardize_label(value):
    value = str(value).strip().lower()

    if value in ["1", "phishing", "spam", "true"]:
        return 1
    if value in ["0", "legitimate", "legit", "ham", "false"]:
        return 0
    
    return None

def clean_dataframe(df: pd.DataFrame, text_col: str, label_col: str, source_name: str, phishing_type_col: str = None) -> pd.DataFrame:
    df = df.copy()
    
    df["text"] = df[text_col].apply(clean_text)
    df["label"] = df[label_col].apply(standardize_label)
    df["source"] = source_name

    if phishing_type_col and phishing_type_col in df.columns:
        df["phishing_type"] = df[phishing_type_col].fillna("unknown")
    else:
        df["phishing_type"] = df["label"].apply(lambda x: "legitimate" if x == 0 else "unknown")
    
    df = df[["text", "label", "source", "phishing_type"]]
    df = df.dropna(subset=["text", "label"])
    df = df[df["text"].str.len() > 10]
    df = df.drop_duplicates(subset=["text"])

    return df