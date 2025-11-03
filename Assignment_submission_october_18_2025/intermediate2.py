'''Intermediate 2: Implement NumPy Fundamentals using a library

You can integrate NumPy arrays with Scikit-learn for machine learning tasks.

Example: Standardizing features before ML.'''


import numpy as np
from sklearn.preprocessing import StandardScaler

# Sample dataset
X = np.array([
    [1, 200],
    [2, 300],
    [3, 400]
])

# Initialize scaler
scaler = StandardScaler()

# Fit and transform the data
X_scaled = scaler.fit_transform(X)

print("Original Data:\n", X)
print("Scaled Data:\n", X_scaled)
