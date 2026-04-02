from data_loader import load_csv
from data_cleaner import clean_dataframe
from data_builder import merge_datasets
from config import RAW_DIR, CLEANED_DIR, FINAL_DIR

from enron_parser import parse_enron_datasets

def main():
    # Synthetic dataset processing
    synthetic_path = f"{RAW_DIR}/synthetic_emails.csv"

    synthetic_df = load_csv(synthetic_path)

    synthetic_clean = clean_dataframe(
        synthetic_df,
        text_col= "text",
        label_col= "label",
        source_name= "synthetic2026",
        phishing_type_col= "phishing_type"
    )

    synthetic_clean.to_csv(f"{CLEANED_DIR}/synthetic_clean.csv", index=False)


    # Enron dataset processing
    enron_path = f"{RAW_DIR}/maildir"

    enron_df = parse_enron_datasets(enron_path, max_emails=5000)

    enron_clean = clean_dataframe(
        enron_df,
        text_col="text",
        label_col="label",
        source_name="enron"
    )

    enron_clean.to_csv(f"{CLEANED_DIR}/enron_clean.csv", index=False)

    # Merging datasets
    final_df = merge_datasets([synthetic_clean, enron_clean])
    final_df.to_csv(f"{FINAL_DIR}/dataset_v2.csv", index=False)
    
    #Validation print statements to check the distribution of dataset after merging
    print("Data pipeline completed. \n")
    print("First 5 rows: ")
    print(final_df.head())
    
    print("\nLabel distribution:")
    print(final_df["label"].value_counts())
    
    print("\nTotal rows: ")
    print(len(final_df))
    
    print("\nMissing values:")
    print(final_df.isnull().sum())

    print("\nPhishing type distribution:")
    print(final_df["phishing_type"].value_counts())

    print("\nSource distribution:")
    print(final_df["source"].value_counts())
    

if __name__ == "__main__":
    main()