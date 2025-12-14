# Simulating a document-based NoSQL dataset (realistic scenario)

sales_data = [
    {"order_id": 1, "product": "Laptop", "price": 900, "region": "US"},
    {"order_id": 2, "product": "Phone", "price": 600, "region": "India"},
    {"order_id": 3, "product": "Laptop", "price": 950, "region": "US"},
    {"order_id": 4, "product": "Tablet", "price": 400, "region": "India"}
]

# Find all Laptop sales
laptops = [order for order in sales_data if order["product"] == "Laptop"]

# Aggregate: total revenue by region
revenue = {}
for order in sales_data:
    revenue[order["region"]] = revenue.get(order["region"], 0) + order["price"]

print("Laptop Orders:", laptops)
print("Revenue by Region:", revenue)
