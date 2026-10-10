
from pathlib import Path
import json
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "logs"


def generate_quality_report():
    df = pd.read_csv(
        DATA_DIR / "online_retail_raw.csv",
        dtype={"InvoiceNo": "string", "StockCode": "string"}
    )

    required_columns = [
        "InvoiceNo", "StockCode", "Quantity",
        "UnitPrice", "InvoiceDate"
    ]

    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    duplicates = df.duplicated(keep="first")

    cancelled = (
        df["InvoiceNo"].str.upper()
        .str.startswith("C", na=False)
    )

    invalid = (
        df["InvoiceNo"].isna()
        | df["StockCode"].isna()
        | df["InvoiceDate"].isna()
        | df["Quantity"].isna()
        | df["UnitPrice"].isna()
        | (df["Quantity"] <= 0)
        | (df["UnitPrice"] <= 0)
    )

    # Cancellation is a valid business event,
    # not automatically a data quality failure.
    rejected_mask = (~cancelled) & invalid & (~duplicates)
    valid_mask = (~cancelled) & (~invalid) & (~duplicates)

    rejected = df.loc[rejected_mask].copy()
    rejected["rejection_reason"] = "Invalid sales transaction"

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    rejected.to_csv(
        DATA_DIR / "rejected_records.csv",
        index=False
    )

    report = {
        "total_records": int(len(df)),
        "duplicate_records": int(duplicates.sum()),
        "cancelled_records": int((cancelled & ~duplicates).sum()),
        "valid_sales_records": int(valid_mask.sum()),
        "rejected_sales_records": int(rejected_mask.sum()),
        "missing_values": {
            k: int(v) for k, v in df.isna().sum().items()
        },
        "valid_sales_rate_percent": round(
            valid_mask.sum() / len(df) * 100, 2
        )
    }

    with open(
        REPORT_DIR / "data_quality_report.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(report, f, indent=4)

    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    generate_quality_report()
