# Mini Project: Weather Data Analyzer

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the dataset
data = pd.read_csv("weather_data.csv")

# Step 2: Display the dataset
print("Weather Data:\n", data)

# Step 3: Calculate basic statistics
avg_temp = data["Temperature"].mean()
max_temp = data["Temperature"].max()
min_temp = data["Temperature"].min()

print(f"\nAverage Temperature: {avg_temp:.2f}°C")
print(f"Highest Temperature: {max_temp}°C")
print(f"Lowest Temperature: {min_temp}°C")

# Step 4: Identify hottest and coldest days
hottest_day = data.loc[data["Temperature"].idxmax(), "Day"]
coldest_day = data.loc[data["Temperature"].idxmin(), "Day"]

print(f"\nHottest Day: {hottest_day}")
print(f"Coldest Day: {coldest_day}")

# Step 5: Plot temperature trend
plt.figure(figsize=(8, 5))
plt.plot(data["Day"], data["Temperature"], marker="o", color="orange", linestyle="-")
plt.title("Weekly Temperature Trend")
plt.xlabel("Day")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.show()
