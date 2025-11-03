#Hard 1: Optimize the implementation of Python Basics & Setup for performance.
import numpy as np
import time

# Step 1: Create a list of numbers from 1 to 1,000,000
numbers = list(range(1, 1_000_001))

# Step 2: Using normal Python sum
start_time = time.time()
python_sum = sum(numbers)
end_time = time.time()
python_time = end_time - start_time
print(f"Normal Python sum = {python_sum}, Time taken = {python_time:.5f} seconds")

# Step 3: Using NumPy vectorized sum
np_numbers = np.array(numbers)
start_time = time.time()
numpy_sum = np.sum(np_numbers)
end_time = time.time()
numpy_time = end_time - start_time
print(f"NumPy sum = {numpy_sum}, Time taken = {numpy_time:.5f} seconds")

# Step 4: Compare results
improvement = (python_time / numpy_time)
print(f"\nNumPy is approximately {improvement:.2f}x faster than normal Python!")
