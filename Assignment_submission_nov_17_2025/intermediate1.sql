CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount INT
);
INSERT INTO customers VALUES
(101, 'Sam'),
(102, 'Rita');

INSERT INTO orders VALUES
(1, 101, 250),
(2, 102, 100),
(3, 101, 300);
SELECT
    c.name,
    SUM(o.amount) AS total_spent,
    RANK() OVER (ORDER BY SUM(o.amount) DESC) AS spending_rank
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.name;
