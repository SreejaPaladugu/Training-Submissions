import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

RAW_CSV = DATA_DIR / "sales_raw.csv"
CLEAN_CSV = DATA_DIR / "sales_clean.csv"

def make_realistic_csv_if_missing():
    if RAW_CSV.exists():
        return

    df = pd.DataFrame([
        {"order_id": 1, "region": "US",    "product": "Laptop", "price": 900, "quantity": 1},
        {"order_id": 2, "region": "India", "product": "Phone",  "price": 600, "quantity": 2},
        {"order_id": 3, "region": "US",    "product": "Laptop", "price": 950, "quantity": 1},
        {"order_id": 4, "region": "India", "product": "Tablet", "price": 400, "quantity": 1},
        {"order_id": 5, "region": "US",    "product": "Phone",  "price": 650, "quantity": 1},
    ])
    df.to_csv(RAW_CSV, index=False)

def extract():
    make_realistic_csv_if_missing()
    return pd.read_csv(RAW_CSV)

def transform(df: pd.DataFrame):
    # basic cleaning + feature engineering
    df = df.copy()
    df["revenue"] = df["price"] * df["quantity"]
    df["product"] = df["product"].str.strip()
    return df

def load(df: pd.DataFrame):
    df.to_csv(CLEAN_CSV, index=False)
    return CLEAN_CSV

def analyze(df: pd.DataFrame):
    # results / insights
    revenue_by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False)
    return revenue_by_region, top_products

def main():
    raw_df = extract()
    clean_df = transform(raw_df)
    out_path = load(clean_df)

    revenue_by_region, top_products = analyze(clean_df)

    print("Saved cleaned dataset to:", out_path)
    print("\nRevenue by region:")
    print(revenue_by_region)

    print("\nRevenue by product:")
    print(top_products)

if __name__ == "__main__":
    main()
