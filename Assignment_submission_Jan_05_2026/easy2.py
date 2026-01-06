import pandas as pd

# 1) Toy transactional sales data (like OLTP)
sales_txn = pd.DataFrame([
    {"order_id": 1, "order_date": "2026-01-01", "customer": "C1", "product": "P1", "qty": 2, "unit_price": 10},
    {"order_id": 2, "order_date": "2026-01-01", "customer": "C2", "product": "P2", "qty": 1, "unit_price": 20},
    {"order_id": 3, "order_date": "2026-01-02", "customer": "C1", "product": "P2", "qty": 3, "unit_price": 20},
])

sales_txn["sales_amount"] = sales_txn["qty"] * sales_txn["unit_price"]

# 2) Build Dimension Tables
dim_customer = sales_txn[["customer"]].drop_duplicates().reset_index(drop=True)
dim_customer["customer_key"] = dim_customer.index + 1

dim_product = sales_txn[["product"]].drop_duplicates().reset_index(drop=True)
dim_product["product_key"] = dim_product.index + 1

dim_date = sales_txn[["order_date"]].drop_duplicates().reset_index(drop=True)
dim_date["date_key"] = dim_date.index + 1

# 3) Build Fact Table (replace natural keys with surrogate keys)
fact_sales = sales_txn.merge(dim_customer, on="customer") \
                     .merge(dim_product, on="product") \
                     .merge(dim_date, on="order_date")

fact_sales = fact_sales[[
    "order_id", "customer_key", "product_key", "date_key", "qty", "unit_price", "sales_amount"
]]

print("DIM CUSTOMER:\n", dim_customer, "\n")
print("DIM PRODUCT:\n", dim_product, "\n")
print("DIM DATE:\n", dim_date, "\n")
print("FACT SALES:\n", fact_sales, "\n")

# 4) Simple warehouse-style query: total sales by product_key
print("Total sales by product_key:")
print(fact_sales.groupby("product_key")["sales_amount"].sum())
