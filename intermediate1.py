import pandas as pd

data = pd.read_csv("student_scores.csv")

print("Dataset Preview:")
print(data.head())
data['Average'] = (data['Math'] + data['Science'] + data['English']) / 3

top_student = data.loc[data['Average'].idxmax(), 'Name']


print("\nStudent Averages:\n", data[['Name', 'Average']])
print(f"\nTop performer: {top_student}")
