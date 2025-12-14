import pandas as pd
import numpy as np
from pathlib import Path
import time

RAW_BIG = Path("data/sales_big_raw.csv")
CLEAN_BIG = Path("data/sales_big_clean.csv")
RAW_BIG.parent.mkdir(exist_ok=True)

def make_big_dataset_if_missing(n=300_000):
    if RAW_BIG.exists():
        return
    rng = np.random.default_rng(42)

    df = pd.DataFrame({
        "order_id": np.arange(1, n + 1),
        "region": rng.choice(["US", "India", "EU"], size=n),
        "product": rng.choice(["Laptop", "Phone", "Tablet", "Monitor"], size=n),
        "price": rng.integers(200, 1500, size=n),
        "quantity": rng.integers(1, 5, size=n),
    })
    df.to_csv(RAW_BIG, index=False)

def extract():
    make_big_dataset_if_missing()
    return pd.read_csv(RAW_BIG)

def transform_optimized(df: pd.DataFrame):
    # Vectorized operations (fast) instead of Python loops (slow)
    df = df.copy()
    df["revenue"] = df["price"] * df["quantity"]
    df["product"] = df["product"].str.strip()

    # Indexing (like DB optimization): make region a categorical type (memory + speed improvement)
    df["region"] = df["region"].astype("category")
    df["product"] = df["product"].astype("category")

    return df

def load(df: pd.DataFrame):
    df.to_csv(CLEAN_BIG, index=False)
    return CLEAN_BIG

def main():
    t0 = time.time()
    df = extract()
    t1 = time.time()

    df2 = transform_optimized(df)
    t2 = time.time()

    out = load(df2)
    t3 = time.time()

    print("Saved:", out)
    print("Timing (seconds):")
    print("  Extract:", round(t1 - t0, 3))
    print("  Transform:", round(t2 - t1, 3))
    print("  Load:", round(t3 - t2, 3))
    print("Rows:", len(df2))

if __name__ == "__main__":
    main()
