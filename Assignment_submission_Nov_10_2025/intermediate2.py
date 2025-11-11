#Intermediate 2: Implement SQL Basics using appropriate library (Scikit-learn, PyTorch, etc.).

import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute("CREATE TABLE Sales (id INT, amount FLOAT)")
cursor.executemany("INSERT INTO Sales VALUES (?, ?)", [(1, 200), (2, 350), (3, 150)])

df = pd.read_sql_query("SELECT AVG(amount) AS avg_sales FROM Sales", conn)
print(df)
conn.close()
