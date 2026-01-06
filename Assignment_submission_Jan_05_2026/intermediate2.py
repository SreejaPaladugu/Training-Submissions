import pandas as pd
import sqlite3

# 1) Sample transactions (can replace with your generated dataset)
sales_txn = pd.DataFrame([
    {"order_id": 1, "order_date": "2026-01-01", "customer": "C1", "product": "P1", "qty": 2, "unit_price": 10},
    {"order_id": 2, "order_date": "2026-01-01", "customer": "C2", "product": "P2", "qty": 1, "unit_price": 20},
    {"order_id": 3, "order_date": "2026-01-02", "customer": "C1", "product": "P2", "qty": 3, "unit_price": 20},
])
sales_txn["sales_amount"] = sales_txn["qty"] * sales_txn["unit_price"]

# 2) Build dimensions
dim_customer = sales_txn[["customer"]].drop_duplicates().reset_index(drop=True)
dim_customer["customer_key"] = dim_customer.index + 1

dim_product = sales_txn[["product"]].drop_duplicates().reset_index(drop=True)
dim_product["product_key"] = dim_product.index + 1

dim_date = sales_txn[["order_date"]].drop_duplicates().reset_index(drop=True)
dim_date["date_key"] = dim_date.index + 1

# 3) Build fact
fact_sales = sales_txn.merge(dim_customer, on="customer") \
                     .merge(dim_product, on="product") \
                     .merge(dim_date, on="order_date")

fact_sales = fact_sales[["order_id", "customer_key", "product_key", "date_key", "qty", "unit_price", "sales_amount"]]

# 4) Load into SQLite (warehouse)
conn = sqlite3.connect("warehouse.db")

dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)
dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)
dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

# 5) Run a warehouse query (join fact + dim)
query = """
SELECT p.product, SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product
ORDER BY total_sales DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

conn.close()
