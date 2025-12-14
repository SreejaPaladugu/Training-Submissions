CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE scores (
    student_id INT,
    subject VARCHAR(50),
    marks INT
);
INSERT INTO students VALUES
(1, 'John'),
(2, 'Anna');

INSERT INTO scores VALUES
(1, 'Math', 90),
(1, 'English', 70),
(2, 'Math', 85);
SELECT 
    s.name,
    AVG(sc.marks) AS avg_marks
FROM students s
LEFT JOIN scores sc
    ON s.student_id = sc.student_id
GROUP BY s.name;
