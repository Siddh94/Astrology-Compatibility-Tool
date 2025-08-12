import pandas as pd
from pathlib import Path

CSV_FILE = Path("data/matches.csv")

def append_to_csv(match_data):
    """Append new match data to CSV file."""
    df_new = pd.DataFrame([match_data])

    if CSV_FILE.exists():
        df_existing = pd.read_csv(CSV_FILE)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    CSV_FILE.parent.mkdir(exist_ok=True)
    df_all.to_csv(CSV_FILE, index=False)
    return CSV_FILE
