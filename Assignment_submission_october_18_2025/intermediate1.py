'''Intermediate 1: Apply NumPy Fundamentals on a real dataset

Example: Use NumPy to analyze a dataset of exam scores.'''

import numpy as np

# Sample dataset: rows are students, columns are subjects
scores = np.array([
    [85, 90, 78],
    [88, 76, 92],
    [70, 80, 85],
    [95, 88, 91]
])

# Compute the average score per student
student_avg = np.mean(scores, axis=1)

# Compute the average score per subject
subject_avg = np.mean(scores, axis=0)

print("Average score per student:", student_avg)
print("Average score per subject:", subject_avg)
