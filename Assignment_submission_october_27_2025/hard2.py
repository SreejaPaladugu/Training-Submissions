import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create synthetic sales dataset
np.random.seed(42)
data = {
    'Date': pd.date_range(start='2024-01-01', periods=100),
    'Product': np.random.choice(['Laptop', 'Tablet', 'Phone', 'Monitor'], 100),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'Units_Sold': np.random.randint(1, 50, 100),
    'Unit_Price': np.random.randint(300, 1200, 100)
}
df = pd.DataFrame(data)

# Step 2: Compute total revenue
df['Revenue'] = df['Units_Sold'] * df['Unit_Price']

# Step 3: Basic cleaning (check for missing values)
print("Missing values:\n", df.isnull().sum())

# Step 4: Analyze top performing products
top_products = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False)
print("\nTotal Revenue by Product:\n", top_products)

# Step 5: Regional performance
regional_sales = df.groupby('Region')['Revenue'].sum()
print("\nRevenue by Region:\n", regional_sales)

# Step 6: Visualization
plt.figure(figsize=(8, 5))
top_products.plot(kind='bar', color='skyblue')
plt.title('Total Revenue by Product')
plt.ylabel('Revenue ($)')
plt.xlabel('Product')
plt.tight_layout()
plt.show()
