# Optimization using indexing (hash-based lookup)

orders = [
    {"order_id": i, "price": i * 10} for i in range(1, 10001)
]

# Build index
order_index = {order["order_id"]: order for order in orders}

# Fast lookup
print(order_index[9999])
