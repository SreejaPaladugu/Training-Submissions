-- Easy 2: Solve a toy example applying SQL Basics.

CREATE TABLE Students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    marks INT
);

INSERT INTO Students VALUES (1, 'Sreeja', 92), (2, 'Anil', 78), (3, 'Riya', 88);

SELECT name, marks 
FROM Students
WHERE marks > 80;
