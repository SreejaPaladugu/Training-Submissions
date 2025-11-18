import pandas as pd

# ===========================
# 1. CREATE DATASETS (TABLES)
# ===========================

products = pd.DataFrame({
    "product_id": [1, 2, 3],
    "category": ["Electronics", "Clothing", "Home"]
})

sales = pd.DataFrame({
    "sale_id": [1, 2, 3, 4],
    "product_id": [1, 1, 2, 3],
    "quantity": [2, 1, 4, 3],
    "price": [500, 500, 50, 100]
})

# ===========================
# 2. JOIN TABLES
# ===========================

merged = sales.merge(products, on="product_id")

# ===========================
# 3. CALCULATE REVENUE
# ===========================

merged["revenue"] = merged["quantity"] * merged["price"]

# ===========================
# 4. GROUP BY CATEGORY
# ===========================

result = merged.groupby("category")["revenue"].sum().reset_index()

# ===========================
# 5. APPLY RANKING
# ===========================

result["rank"] = result["revenue"].rank(ascending=False, method="dense")

# ===========================
# 6. PRINT FINAL RESULT
# ===========================

print("FINAL OUTPUT:")
print(result)
