import sqlite3
import pandas as pd

conn = sqlite3.connect("warehouse.db")
cur = conn.cursor()

# 1) Create indexes (speed up joins & filters)
cur.execute("CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_sales(product_key);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_sales(customer_key);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_sales(date_key);")

# 2) Create a pre-aggregated table (like a summary table / materialized view)
cur.execute("DROP TABLE IF EXISTS agg_sales_by_product;")
cur.execute("""
CREATE TABLE agg_sales_by_product AS
SELECT product_key, SUM(sales_amount) AS total_sales
FROM fact_sales
GROUP BY product_key;
""")

# 3) Query becomes faster (no big scans over fact table)
query = """
SELECT p.product, a.total_sales
FROM agg_sales_by_product a
JOIN dim_product p ON a.product_key = p.product_key
ORDER BY a.total_sales DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

conn.commit()
conn.close()
