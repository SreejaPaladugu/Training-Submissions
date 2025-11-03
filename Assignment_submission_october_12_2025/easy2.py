#Solve a toy example applying Python Data Structures.
students = [("Alice", "Math"),("Bob", "Science"),("Alice", "English"),("Charlie", "Math")]

subjects_by_student = {}
for name, subject in students:
    subjects_by_student.setdefault(name, set()).add(subject)

print(subjects_by_student)