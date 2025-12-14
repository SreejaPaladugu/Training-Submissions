# Toy NoSQL example using a Python dictionary (key-value store)

user_db = {
    "user_101": {"name": "Alice", "age": 25},
    "user_102": {"name": "Bob", "age": 30}
}

# Insert (Create)
user_db["user_103"] = {"name": "Charlie", "age": 28}

# Read
print("User 101:", user_db["user_101"])

# Update
user_db["user_102"]["age"] = 31

# Delete
del user_db["user_101"]

print("Final Database:", user_db)
