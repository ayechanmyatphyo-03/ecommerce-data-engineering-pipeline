
from pathlib import Path
import pandas as pd

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output file paths
RAW_FILE = BASE_DIR / "data" / "raw" / "online_retail.xlsx"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "online_retail_raw.csv"

def extract_data():
    print("Starting data extraction...")

    if not RAW_FILE.exists():
        raise FileNotFoundError(f"File not found: {RAW_FILE}")

    # Extract data from Excel
    df = pd.read_excel(RAW_FILE, engine="openpyxl")

    print(f"Rows extracted: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Display first five rows
    print("\nFirst 5 rows:")
    print(df.head())

    # Display missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Save extracted data as CSV
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nData saved to: {OUTPUT_FILE}")

    return df

if __name__ == "__main__":
    extract_data()
