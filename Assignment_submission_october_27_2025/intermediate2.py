from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load the Iris dataset
iris = load_iris()

# Convert to a Pandas DataFrame
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target

# Display first few rows
print(df.head())

# Apply scaling using Scikit-learn
scaler = StandardScaler()
df[iris.feature_names] = scaler.fit_transform(df[iris.feature_names])

# Verify scaled results
print(df.describe())

