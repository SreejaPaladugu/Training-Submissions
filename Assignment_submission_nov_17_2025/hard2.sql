-- CREATE TABLES
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name TEXT
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name TEXT,
    dept_id INT
);

CREATE TABLE salary_payments (
    payment_id INT PRIMARY KEY,
    emp_id INT,
    payment_date TEXT,
    amount INT
);

-- INSERT DATA
INSERT INTO departments VALUES
(1, 'Engineering'),
(2, 'HR'),
(3, 'Finance');

INSERT INTO employees VALUES
(101, 'Alice', 1),
(102, 'Bob', 1),
(103, 'Carol', 2),
(104, 'David', 3);

INSERT INTO salary_payments VALUES
(1, 101, '2023-01-15', 5000),
(2, 101, '2023-04-15', 5200),
(3, 102, '2023-01-18', 4800),
(4, 102, '2023-04-18', 5000),
(5, 103, '2023-02-10', 3000),
(6, 104, '2023-07-20', 7000);

-- FINAL MINI PROJECT QUERY: Quarterly salary + QoQ growth for SQLite

WITH full_data AS (
    SELECT
        d.dept_name,
        sp.amount,
        sp.payment_date,
        strftime('%Y', sp.payment_date) AS yr,
        CASE
            WHEN strftime('%m', sp.payment_date) BETWEEN '01' AND '03' THEN 'Q1'
            WHEN strftime('%m', sp.payment_date) BETWEEN '04' AND '06' THEN 'Q2'
            WHEN strftime('%m', sp.payment_date) BETWEEN '07' AND '09' THEN 'Q3'
            ELSE 'Q4'
        END AS qtr
    FROM salary_payments sp
    JOIN employees e ON sp.emp_id = e.emp_id
    JOIN departments d ON e.dept_id = d.dept_id
),
quarterly AS (
    SELECT
        dept_name,
        yr || qtr AS quarter,
        SUM(amount) AS total_salary
    FROM full_data
    GROUP BY dept_name, yr, qtr
),
joined AS (
    SELECT
        a.dept_name,
        a.quarter,
        a.total_salary,
        b.total_salary AS previous_salary
    FROM quarterly a
    LEFT JOIN quarterly b
        ON a.dept_name = b.dept_name
        AND (
            (CAST(substr(a.quarter,1,4) AS INT) = CAST(substr(b.quarter,1,4) AS INT) AND
             substr(a.quarter,5,2) = 'Q2' AND substr(b.quarter,5,2) = 'Q1')
         OR (substr(a.quarter,5,2) = 'Q3' AND substr(b.quarter,5,2) = 'Q2' AND substr(a.quarter,1,4)=substr(b.quarter,1,4))
         OR (substr(a.quarter,5,2) = 'Q4' AND substr(b.quarter,5,2) = 'Q3' AND substr(a.quarter,1,4)=substr(b.quarter,1,4))
        )
)
SELECT
    dept_name,
    quarter,
    total_salary,
    CASE
        WHEN previous_salary IS NULL THEN NULL
        ELSE ROUND(((total_salary - previous_salary) * 100.0) / previous_salary, 2)
    END AS qoq_growth_pct
FROM joined
ORDER BY dept_name, quarter;
