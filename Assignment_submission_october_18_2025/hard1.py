'''Hard 1: Optimize implementation for performance

Scenario: Suppose you want to compute the sum of squares of a large array.'''


import numpy as np

# Large array
arr = np.random.rand(1_000_000)

# Vectorized implementation (fast)
sum_squares = np.sum(arr**2)

print("Sum of squares:", sum_squares)
 