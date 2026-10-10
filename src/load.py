
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

csv_path = BASE_DIR / "data" / "processed" / "cleaned_sales.csv"

df = pd.read_csv(csv_path)

database_url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(database_url)

df.to_sql(
    "sales",
    engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print("Data loaded successfully!")
print("Total rows:", len(df))
