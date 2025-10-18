'''Easy 2: Solve a toy example applying NumPy Fundamentals

Example: Compute the element-wise sum and mean of two arrays.'''

import numpy as np

# Create two arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Element-wise sum
sum_ab = a + b  # [5, 7, 9]

# Mean of the sum
mean_sum = np.mean(sum_ab)  # 7.0

print("Sum:", sum_ab)
print("Mean:", mean_sum)
