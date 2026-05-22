"""
This file handles loading CSV files for the data pipeline.

I kept this small so the other data scripts can reuse the same loading function.
"""

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)