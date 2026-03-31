from data_loader import load_csv
from data_cleaner import clean_dataframe
from data_builder import merge_datasets
from config import RAW_DIR, CLEANED_DIR, FINAL_DIR

def main():
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

    final_df = merge_datasets([synthetic_clean])
    final_df.to_csv(f"{FINAL_DIR}/dataset_v1.csv", index=False)
    
    print("Data pipeline completed. \n")
    print("First 5 rows: ")
    print(final_df.head())
    print("\nLabel distribution:")
    
    #Validation print statements to check the distribution of labels
    print("\nTotal rows: ")
    print(len(final_df))
    
    print("\nMissing values:")
    print(final_df.isnull().sum())

    print("\nPhishing type distribution:")
    print(final_df["phishing_type"].value_counts())
    
    print(final_df["label"].value_counts())

if __name__ == "__main__":
    main()

