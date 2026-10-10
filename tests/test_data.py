
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "processed" / "cleaned_sales.csv"


@pytest.fixture(scope="module")
def sales_data():
    assert CSV_PATH.exists(), "cleaned_sales.csv not found!"

    return pd.read_csv(
        CSV_PATH,
        dtype={"InvoiceNo": "string"},
        low_memory=False
    )


def test_dataset_not_empty(sales_data):
    assert len(sales_data) > 0


def test_required_columns(sales_data):
    required_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
        "TotalAmount"
    ]

    for column in required_columns:
        assert column in sales_data.columns


def test_no_invalid_quantity(sales_data):
    assert (sales_data["Quantity"] > 0).all()


def test_no_invalid_price(sales_data):
    assert (sales_data["UnitPrice"] > 0).all()


def test_no_missing_invoice(sales_data):
    assert sales_data["InvoiceNo"].notna().all()


def test_no_cancelled_orders(sales_data):
    assert not sales_data["InvoiceNo"].str.startswith(
        "C", na=False
    ).any()


def test_total_amount_calculation(sales_data):
    expected = (
        sales_data["Quantity"] * sales_data["UnitPrice"]
    )

    assert np.allclose(
        sales_data["TotalAmount"],
        expected,
        rtol=0,
        atol=1e-8
    )


def test_no_duplicate_records(sales_data):
    assert not sales_data.duplicated().any()
