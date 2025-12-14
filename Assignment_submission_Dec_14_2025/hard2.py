import pandas as pd
from pathlib import Path
from datetime import datetime
import time

DATA_DIR = Path("project_data")
OUT_DIR = Path("project_output")
DATA_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

RAW = DATA_DIR / "customers_raw.csv"
CURATED = OUT_DIR / "customers_curated.csv"
REPORT = OUT_DIR / "quality_report.txt"

# ---------- Create sample raw data ----------
def seed_data_if_missing():
    if RAW.exists():
        return
    df = pd.DataFrame([
        {"customer_id": 1, "name": " alice ", "country": "US", "age": 25, "spend": 1200},
        {"customer_id": 2, "name": "BOB",     "country": "India", "age": None, "spend": 800},
        {"customer_id": 3, "name": "cathy",   "country": "US", "age": 31, "spend": 2200},
        {"customer_id": 4, "name": "dan",     "country": "EU", "age": 29, "spend": 500},
    ])
    df.to_csv(RAW, index=False)

# ---------- Airflow-like DAG runner ----------
class Task:
    def __init__(self, name, fn, retries=1, retry_delay_sec=1):
        self.name = name
        self.fn = fn
        self.retries = retries
        self.retry_delay_sec = retry_delay_sec

def run_task(task: Task, context: dict):
    attempt = 0
    while True:
        try:
            attempt += 1
            print(f"[{datetime.now()}] START {task.name} (attempt {attempt})")
            result = task.fn(context)
            print(f"[{datetime.now()}] END   {task.name}\n")
            return result
        except Exception as e:
            print(f"[{datetime.now()}] ERROR in {task.name}: {e}")
            if attempt > task.retries:
                raise
            time.sleep(task.retry_delay_sec)

# ---------- ETL tasks ----------
def extract_task(context):
    seed_data_if_missing()
    df = pd.read_csv(RAW)
    context["raw_df"] = df
    return df

def transform_task(context):
    df = context["raw_df"].copy()

    # cleaning
    df["name"] = df["name"].astype(str).str.strip().str.title()
    df["country"] = df["country"].astype(str).str.strip().str.upper()

    # fill missing ages with median
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["age"] = df["age"].fillna(df["age"].median())

    # feature: segment
    df["segment"] = pd.cut(df["spend"], bins=[-1, 700, 1500, 10_000], labels=["Low", "Mid", "High"])

    context["curated_df"] = df
    return df

def data_quality_task(context):
    df = context["curated_df"]

    checks = {
        "row_count": len(df),
        "nulls_per_column": df.isna().sum().to_dict(),
        "duplicate_customer_ids": int(df["customer_id"].duplicated().sum()),
    }

    report_lines = [
        "DATA QUALITY REPORT",
        f"Generated: {datetime.now()}",
        f"Row count: {checks['row_count']}",
        f"Duplicate customer_id count: {checks['duplicate_customer_ids']}",
        f"Nulls per column: {checks['nulls_per_column']}",
    ]
    REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    context["quality_checks"] = checks
    return checks

def load_task(context):
    df = context["curated_df"]
    df.to_csv(CURATED, index=False)
    return CURATED

def main():
    context = {}

    dag = [
        Task("extract_task", extract_task, retries=1),
        Task("transform_task", transform_task, retries=1),
        Task("data_quality_task", data_quality_task, retries=1),
        Task("load_task", load_task, retries=1),
    ]

    for t in dag:
        run_task(t, context)

    print("Pipeline complete.")
    print("Curated output:", CURATED)
    print("Quality report:", REPORT)

if __name__ == "__main__":
    main()
