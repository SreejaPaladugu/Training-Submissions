import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from pathlib import Path

CLEAN_CSV = Path("data/sales_clean.csv")

def extract():
    if not CLEAN_CSV.exists():
        raise FileNotFoundError("Run intermediate1_real_dataset_etl.py first to generate data/sales_clean.csv")
    return pd.read_csv(CLEAN_CSV)

def transform_for_ml(df: pd.DataFrame):
    # Features / label
    X = df[["region", "product", "quantity", "price"]]
    y = df["revenue"]
    return X, y

def train_model(X, y):
    cat_cols = ["region", "product"]
    num_cols = ["quantity", "price"]

    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )

    model = Pipeline(steps=[
        ("preprocess", pre),
        ("regressor", LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    return mae

def main():
    df = extract()
    X, y = transform_for_ml(df)
    mae = train_model(X, y)
    print("Model trained successfully.")
    print("MAE (lower is better):", round(mae, 2))

if __name__ == "__main__":
    main()
