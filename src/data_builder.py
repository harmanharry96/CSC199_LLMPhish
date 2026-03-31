import pandas as pd

def merge_datasets(datasets: list[pd.DataFrame]) -> pd.DataFrame:
    final_df = pd.concat(datasets, ignore_index=True)
    final_df = final_df.drop_duplicates(subset=["text"])
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
    return final_df
