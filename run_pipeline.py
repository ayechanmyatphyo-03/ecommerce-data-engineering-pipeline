
import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / "pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

STEPS = [
    ("Extract Data", "src/extract.py"),
    ("Transform Data", "src/transform.py"),
    ("Data Quality Report", "src/data_quality.py"),
    ("Data Tests", "tests/test_data.py"),
    ("Load to PostgreSQL", "src/load.py"),
    ("Run SQL Queries", "src/run_queries.py"),
    ("Validate Database", "src/validate_db.py"),
]


def run_step(name, script):
    logging.info("Starting: %s", name)

    result = subprocess.run(
        [sys.executable, str(BASE_DIR / script)],
        cwd=BASE_DIR,
        check=False
    )

    if result.returncode != 0:
        logging.error("FAILED: %s", name)
        raise RuntimeError(
            f"Pipeline stopped at: {name}"
        )

    logging.info("SUCCESS: %s", name)


def main():
    start = datetime.now()

    logging.info("=" * 45)
    logging.info("E-COMMERCE ETL PIPELINE STARTED")
    logging.info("=" * 45)

    try:
        for name, script in STEPS:
            run_step(name, script)

    except Exception:
        logging.exception("PIPELINE FAILED")
        sys.exit(1)

    duration = (datetime.now() - start).total_seconds()

    logging.info("=" * 45)
    logging.info("PIPELINE COMPLETED SUCCESSFULLY")
    logging.info("Execution time: %.2f seconds", duration)
    logging.info("=" * 45)


if __name__ == "__main__":
    main()
