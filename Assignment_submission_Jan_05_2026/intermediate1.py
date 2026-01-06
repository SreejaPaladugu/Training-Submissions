import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(7)

# 1) Generate realistic transactions
n = 1000
customers = [f"C{c}" for c in range(1, 51)]     # 50 customers
products = [f"P{p}" for p in range(1, 21)]      # 20 products
start_date = datetime(2025, 11, 1)

rows = []
for i in range(1, n + 1):
    order_date = start_date + timedelta(days=random.randint(0, 60))
    cust = random.choice(customers)
    prod = random.choice(products)
    qty = random.randint(1, 5)
    unit_price = random.choice([10, 15, 20, 25, 30])
    rows.append({
        "order_id": i,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer": cust,
        "product": prod,
        "qty": qty,
        "unit_price": unit_price
    })

sales_txn = pd.DataFrame(rows)
sales_txn["sales_amount"] = sales_txn["qty"] * sales_txn["unit_price"]

# 2) Dimensions
dim_customer = sales_txn[["customer"]].drop_duplicates().reset_index(drop=True)
dim_customer["customer_key"] = dim_customer.index + 1

dim_product = sales_txn[["product"]].drop_duplicates().reset_index(drop=True)
dim_product["product_key"] = dim_product.index + 1

dim_date = sales_txn[["order_date"]].drop_duplicates().reset_index(drop=True)
dim_date["date_key"] = dim_date.index + 1

# 3) Fact
fact_sales = sales_txn.merge(dim_customer, on="customer") \
                     .merge(dim_product, on="product") \
                     .merge(dim_date, on="order_date")

fact_sales = fact_sales[[
    "order_id", "customer_key", "product_key", "date_key", "qty", "unit_price", "sales_amount"
]]

# 4) Analytics (warehouse queries)
total_revenue = fact_sales["sales_amount"].sum()

top_products = fact_sales.groupby("product_key")["sales_amount"].sum().sort_values(ascending=False).head(5)
top_customers = fact_sales.groupby("customer_key")["sales_amount"].sum().sort_values(ascending=False).head(5)

print("TOTAL REVENUE:", total_revenue)
print("\nTOP 5 PRODUCTS (by revenue):\n", top_products)
print("\nTOP 5 CUSTOMERS (by revenue):\n", top_customers)
