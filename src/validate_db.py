
import os
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

csv_path = BASE_DIR / "data/processed/cleaned_sales.csv"
df = pd.read_csv(
    csv_path,
    dtype={"InvoiceNo": "string"},
    low_memory=False
)

url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url)

query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (
        WHERE "TotalAmount" IS NULL
           OR "InvoiceNo" IS NULL
           OR "InvoiceDate" IS NULL
    ) AS null_rows,
    COUNT(*) FILTER (
        WHERE "Quantity" <= 0
           OR "UnitPrice" <= 0
           OR "TotalAmount" <= 0
    ) AS invalid_sales,
    SUM("TotalAmount") AS total_revenue
FROM sales
"""

with engine.connect() as conn:
    result = pd.read_sql_query(text(query), conn).iloc[0]

assert int(result["total_rows"]) == len(df), \
    "Row count mismatch!"

assert int(result["null_rows"]) == 0, \
    "Null values detected!"

assert int(result["invalid_sales"]) == 0, \
    "Invalid sales detected!"

assert np.isclose(
    float(result["total_revenue"]),
    float(df["TotalAmount"].sum()),
    rtol=0,
    atol=0.01
), "Revenue mismatch!"

print("All database validation checks passed!")
print("Validated rows:", int(result["total_rows"]))
