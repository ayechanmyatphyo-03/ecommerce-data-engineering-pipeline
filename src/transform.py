
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "online_retail_raw.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"


def transform_data():
    print("Starting data transformation...")

    # 1. Extract CSV
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(
        INPUT_FILE,
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "CustomerID": "string"
        }
    )

    print(f"Original rows: {len(df):,}")

    # 2. Validate required columns
    required_columns = [
        "InvoiceNo", "StockCode", "Description",
        "Quantity", "InvoiceDate", "UnitPrice",
        "CustomerID", "Country"
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # 3. Data quality report
    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    # 4. Remove exact duplicates
    df = df.drop_duplicates().copy()

    # 5. Convert data types
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    # 6. Identify cancelled orders
    df["IsCancelled"] = (
        df["InvoiceNo"]
        .str.upper()
        .str.startswith("C", na=False)
    )

    # 7. Separate valid sales
    valid_sales = df[
        (~df["IsCancelled"]) &
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0) &
        (df["InvoiceDate"].notna()) &
        (df["InvoiceNo"].notna()) &
        (df["StockCode"].notna())
    ].copy()

    # 8. Calculate revenue
    valid_sales["TotalAmount"] = (
        valid_sales["Quantity"] *
        valid_sales["UnitPrice"]
    )

    # 9. Create date features
    valid_sales["Year"] = valid_sales["InvoiceDate"].dt.year
    valid_sales["Month"] = valid_sales["InvoiceDate"].dt.month

    # 10. Separate cancelled transactions
    cancelled_orders = df[
        df["IsCancelled"]
    ].copy()

    # 11. Save processed files
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    valid_sales.to_csv(
        OUTPUT_DIR / "cleaned_sales.csv",
        index=False
    )

    cancelled_orders.to_csv(
        OUTPUT_DIR / "cancelled_orders.csv",
        index=False
    )

    print("\nTransformation completed!")
    print(f"Valid sales rows: {len(valid_sales):,}")
    print(f"Cancelled rows: {len(cancelled_orders):,}")

    print("\nFirst 5 cleaned records:")
    print(valid_sales.head())

    return valid_sales


if __name__ == "__main__":
    transform_data()
