-- Intermediate 1: Apply SQL Basics on a real dataset and explain results.
-- Create a simple Sales table
CREATE TABLE Sales (
    id INTEGER PRIMARY KEY,
    region TEXT,
    product TEXT,
    quantity INTEGER,
    price_per_unit DECIMAL(10,2),
    sale_date TEXT
);

-- Insert sample data
INSERT INTO Sales VALUES
(1, 'North', 'Laptop', 2, 900.00, '2024-09-10'),
(2, 'South', 'Mouse', 5, 25.00, '2024-09-11'),
(3, 'East', 'Keyboard', 3, 45.00, '2024-09-12'),
(4, 'West', 'Monitor', 1, 200.00, '2024-09-13'),
(5, 'North', 'Mouse', 4, 25.00, '2024-09-14'),
(6, 'South', 'Laptop', 1, 900.00, '2024-09-15'),
(7, 'East', 'Monitor', 2, 200.00, '2024-09-16'),
(8, 'West', 'Keyboard', 5, 45.00, '2024-09-17'),
(9, 'North', 'Monitor', 3, 200.00, '2024-09-18'),
(10, 'South', 'Laptop', 1, 900.00, '2024-09-19');

-- View all sales
SELECT * FROM Sales;

-- Calculate total revenue (quantity * price_per_unit)
SELECT SUM(quantity * price_per_unit) AS total_revenue FROM Sales;

-- Find total sales per region
SELECT region, SUM(quantity * price_per_unit) AS revenue
FROM Sales
GROUP BY region
ORDER BY revenue DESC;

-- Find most sold product by quantity
SELECT product, SUM(quantity) AS total_sold
FROM Sales
GROUP BY product
ORDER BY total_sold DESC;

-- Average sale amount per transaction
SELECT ROUND(AVG(quantity * price_per_unit), 2) AS avg_sale_value FROM Sales;
