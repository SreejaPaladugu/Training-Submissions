import pandas as pd
import sqlite3
import random
from datetime import datetime, timedelta

random.seed(10)

def generate_transactions(n=2000):
    customers = [f"C{c}" for c in range(1, 101)]
    products = [f"P{p}" for p in range(1, 31)]
    start_date = datetime(2025, 10, 1)

    rows = []
    for i in range(1, n + 1):
        order_date = start_date + timedelta(days=random.randint(0, 90))
        rows.append({
            "order_id": i,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "customer": random.choice(customers),
            "product": random.choice(products),
            "qty": random.randint(1, 6),
            "unit_price": random.choice([10, 15, 20, 25, 30, 40])
        })

    df = pd.DataFrame(rows)
    df["sales_amount"] = df["qty"] * df["unit_price"]
    return df

def build_star_schema(sales_txn: pd.DataFrame):
    dim_customer = sales_txn[["customer"]].drop_duplicates().reset_index(drop=True)
    dim_customer["customer_key"] = dim_customer.index + 1

    dim_product = sales_txn[["product"]].drop_duplicates().reset_index(drop=True)
    dim_product["product_key"] = dim_product.index + 1

    dim_date = sales_txn[["order_date"]].drop_duplicates().reset_index(drop=True)
    dim_date["date_key"] = dim_date.index + 1

    fact_sales = sales_txn.merge(dim_customer, on="customer") \
                         .merge(dim_product, on="product") \
                         .merge(dim_date, on="order_date")

    fact_sales = fact_sales[["order_id", "customer_key", "product_key", "date_key", "qty", "unit_price", "sales_amount"]]
    return dim_customer, dim_product, dim_date, fact_sales

def load_to_sqlite(dim_customer, dim_product, dim_date, fact_sales, db_name="dw_mini_project.db"):
    conn = sqlite3.connect(db_name)
    dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)
    dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
    fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_sales(product_key);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_sales(customer_key);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_sales(date_key);")
    conn.commit()
    return conn

def run_kpis(conn):
    kpi_queries = {
        "total_revenue": "SELECT SUM(sales_amount) AS total_revenue FROM fact_sales;",
        "top_products": """
            SELECT p.product, SUM(f.sales_amount) AS total_sales
            FROM fact_sales f
            JOIN dim_product p ON f.product_key = p.product_key
            GROUP BY p.product
            ORDER BY total_sales DESC
            LIMIT 10;
        """,
        "top_customers": """
            SELECT c.customer, SUM(f.sales_amount) AS total_sales
            FROM fact_sales f
            JOIN dim_customer c ON f.customer_key = c.customer_key
            GROUP BY c.customer
            ORDER BY total_sales DESC
            LIMIT 10;
        """
    }

    total_rev = pd.read_sql_query(kpi_queries["total_revenue"], conn)
    top_products = pd.read_sql_query(kpi_queries["top_products"], conn)
    top_customers = pd.read_sql_query(kpi_queries["top_customers"], conn)

    return total_rev, top_products, top_customers

if __name__ == "__main__":
    # 1) Extract
    sales_txn = generate_transactions(n=2000)

    # 2) Transform (star schema)
    dim_customer, dim_product, dim_date, fact_sales = build_star_schema(sales_txn)

    # 3) Load
    conn = load_to_sqlite(dim_customer, dim_product, dim_date, fact_sales)

    # 4) Analytics / KPIs
    total_rev, top_products, top_customers = run_kpis(conn)

    print("TOTAL REVENUE:\n", total_rev, "\n")
    print("TOP PRODUCTS:\n", top_products, "\n")
    print("TOP CUSTOMERS:\n", top_customers, "\n")

    # 5) Export KPIs to CSV (report artifact)
    top_products.to_csv("kpi_top_products.csv", index=False)
    top_customers.to_csv("kpi_top_customers.csv", index=False)

    conn.close()
    print("Exported: kpi_top_products.csv, kpi_top_customers.csv")
