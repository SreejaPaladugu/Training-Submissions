# Mini NoSQL Project: Customer Order System

orders = []

def create_order(order_id, customer, amount):
    orders.append({
        "order_id": order_id,
        "customer": customer,
        "amount": amount
    })

def get_customer_orders(customer):
    return [o for o in orders if o["customer"] == customer]

def total_revenue():
    return sum(o["amount"] for o in orders)

# Operations
create_order(1, "Alice", 500)
create_order(2, "Bob", 700)
create_order(3, "Alice", 300)

print("Alice Orders:", get_customer_orders("Alice"))
print("Total Revenue:", total_revenue())
