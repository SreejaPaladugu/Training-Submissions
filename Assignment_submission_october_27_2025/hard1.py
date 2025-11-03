import pandas as pd
import numpy as np
import time

# Create a large synthetic dataset
df = pd.DataFrame({
    'col1': np.random.randint(1, 1000, 1_000_000),
    'col2': np.random.rand(1_000_000)
})

# Example 1: Non-optimized (loop-based)
start = time.time()
df['new_col_loop'] = [x * 2 for x in df['col1']]
print("Loop time:", round(time.time() - start, 3), "seconds")

# Example 2: Optimized (vectorized)
start = time.time()
df['new_col_vectorized'] = df['col1'] * 2
print("Vectorized time:", round(time.time() - start, 3), "seconds")
