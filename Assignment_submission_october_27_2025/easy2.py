import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 22],
        'City': ['NY', 'LA', 'SF']}
df = pd.DataFrame(data)

print(df)
print("Average Age:", df['Age'].mean())
