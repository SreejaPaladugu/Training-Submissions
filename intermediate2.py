# Intermediate 2: Implement Python Basics & Setup using appropriate library (Scikit-learn, PyTorch, etc.).
import matplotlib.pyplot as plt

# Step 1: Create sample data
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sales = [250, 300, 280, 350, 400, 500, 450]

# Step 2: Use basic Python to calculate statistics
total_sales = sum(sales)
avg_sales = total_sales / len(sales)

print(f"Total weekly sales: ${total_sales}")
print(f"Average daily sales: ${avg_sales:.2f}")

# Step 3: Plot the data
plt.plot(days, sales, marker='o', color='blue', linestyle='--')
plt.title("Weekly Sales Trend")
plt.xlabel("Day")
plt.ylabel("Sales ($)")
plt.grid(True)

# Step 4: Show the chart
plt.show()
