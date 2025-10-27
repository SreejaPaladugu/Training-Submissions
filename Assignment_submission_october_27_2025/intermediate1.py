import pandas as pd

# Load Titanic dataset directly from GitHub
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Display basic info and summary statistics
print(df.info())
print(df.describe())

# Analyze survival counts and rates by gender
print(df['Survived'].value_counts())
print(df.groupby('Sex')['Survived'].mean())
