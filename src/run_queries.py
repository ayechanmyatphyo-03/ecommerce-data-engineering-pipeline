
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url)

queries = {
    "total_rows": """
        SELECT COUNT(*) AS total_rows
        FROM sales
    """,
    "total_revenue": """
        SELECT ROUND(SUM("TotalAmount")::numeric, 2)
        AS total_revenue
        FROM sales
    """,
    "top_products": """
        SELECT "Description",
               ROUND(SUM("TotalAmount")::numeric, 2)
               AS revenue
        FROM sales
        GROUP BY "Description"
        ORDER BY revenue DESC
        LIMIT 10
    """,
    "monthly_revenue": """
        SELECT
            DATE_TRUNC('month',
                "InvoiceDate"::timestamp) AS month,
            ROUND(SUM("TotalAmount")::numeric, 2)
                AS revenue
        FROM sales
        GROUP BY month
        ORDER BY month
    """
}

output_dir = BASE_DIR / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

with engine.connect() as conn:
    for name, query in queries.items():
        df = pd.read_sql_query(text(query), conn)

        print(f"\n{name.upper()}")
        print(df.head(10).to_string(index=False))

        df.to_csv(output_dir / f"{name}.csv", index=False)

print("\nAll SQL queries completed successfully!")
