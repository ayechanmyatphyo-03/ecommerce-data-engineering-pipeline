
# E-Commerce Data Engineering Pipeline

An end-to-end ETL pipeline built with Python, Pandas, PostgreSQL, and SQLAlchemy to process, validate, and analyze real-world e-commerce transaction data.

## Project Overview

This project demonstrates the design and implementation of a reproducible data engineering workflow, from raw Excel ingestion to PostgreSQL storage, SQL analytics, automated testing, and data quality validation.

## Tech Stack

- Python
- Pandas and NumPy
- PostgreSQL 18
- SQLAlchemy and psycopg2
- SQL
- pytest
- Python logging
- python-dotenv

## Dataset

Source: UCI Machine Learning Repository — Online Retail Dataset

https://archive.ics.uci.edu/dataset/352/online+retail

- Original records: 541,909
- Validated sales records: 524,878
- Period: December 2010 – December 2011
- Dataset type: E-commerce transactions

The dataset contains invoice numbers, products, quantities, unit prices, customer IDs, countries, and transaction timestamps.

## Pipeline Architecture

Raw Excel Dataset
    |
    v
Extract Data (extract.py)
    |
    v
Transform Data (transform.py)
    |
    v
Data Quality Report (data_quality.py)
    |
    v
Automated Tests (pytest)
    |
    v
PostgreSQL Load (load.py)
    |
    v
SQL Analytics (run_queries.py)
    |
    v
Database Validation (validate_db.py)

## Key Features

### Data Extraction
- Reads transaction data from Excel
- Exports raw data to CSV

### Data Transformation
- Removes duplicate records
- Identifies cancelled transactions
- Filters invalid quantities and prices
- Calculates transaction revenue
- Generates cleaned datasets

### Database Integration
- Connects Python to PostgreSQL
- Loads cleaned sales into a relational database
- Supports SQL-based analysis

### Data Quality
- Generates JSON quality reports
- Tracks missing and rejected records
- Validates row counts and revenue totals

### Automated Testing
- Eight pytest checks
- Required column validation
- Positive quantity and price checks
- Duplicate detection
- Revenue calculation verification

### Pipeline Automation
- Executes the workflow from a single command
- Logs execution results
- Stops on failed steps

## Project Structure

ecommerce-data-pipeline/
    data/
        raw/
        processed/
    src/
        extract.py
        transform.py
        data_quality.py
        load.py
        queries.sql
        run_queries.py
        validate_db.py
    tests/
        test_data.py
    logs/
    docs/
    run_pipeline.py
    requirements.txt
    README.md
    .gitignore

## Installation

Clone the repository and create a Python virtual environment.

Install dependencies:

    python -m pip install -r requirements.txt

Create a local .env file:

    DB_HOST=localhost
    DB_PORT=5433
    DB_NAME=ecommerce_db
    DB_USER=postgres
    DB_PASSWORD=your_password

Set DB_PORT to the port used by your PostgreSQL server.

Download the Online Retail dataset from UCI and save the Excel file as:

    data/raw/online_retail.xlsx

Create the PostgreSQL database before running the pipeline.

## Run the Pipeline

    python run_pipeline.py

## Run Automated Tests

    python -m pytest tests/ -v

## SQL Analytics

The project generates:
- Total transaction count
- Total revenue
- Top 10 products by revenue
- Monthly revenue trends

## Validation Results

- Database records validated: 524,878
- Automated tests: 8 passed
- Database validation: passed
- Pipeline execution time: 127.35 seconds

These results reflect one successful local execution.

## Future Improvements

- Incremental data loading
- PostgreSQL schema constraints
- Docker containerization
- CI/CD using GitHub Actions
- Workflow orchestration using Apache Airflow
- Cloud deployment

## Author

Aye Chan Myat Phyo

BSc (Hons) Data Science & Artificial Intelligence
University of the West of England (UWE Bristol)
