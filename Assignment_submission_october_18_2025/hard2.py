'''Hard 2: Build a mini project applying NumPy end-to-end

Mini project idea: Student Exam Data Analyzer
Steps:

Generate random exam scores for 100 students across 5 subjects using NumPy.

Compute per-student average, per-subject average, and top performers.

Identify students who scored below the class average.'''

import numpy as np

# Step 1: Generate data
np.random.seed(0)
scores = np.random.randint(50, 101, (100, 5))  # 100 students, 5 subjects

# Step 2: Compute averages
student_avg = np.mean(scores, axis=1)
subject_avg = np.mean(scores, axis=0)

# Step 3: Top performers (students with average > 90)
top_students = np.where(student_avg > 90)[0]

# Step 4: Students below class average
class_avg = np.mean(student_avg)
below_avg_students = np.where(student_avg < class_avg)[0]

print("Subject averages:", subject_avg)
print("Top students (index):", top_students)
print("Students below class average (index):", below_avg_students)
