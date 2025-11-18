CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    price INT
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    category VARCHAR(50)
);
INSERT INTO order_items VALUES
(1, 1, 2, 300),
(1, 2, 1, 150),
(2, 1, 1, 300),
(3, 3, 5, 20);

INSERT INTO products VALUES
(1, 'Electronics'),
(2, 'Home'),
(3, 'Clothing');
WITH item_rev AS (
    SELECT 
        product_id,
        SUM(quantity * price) AS revenue
    FROM order_items
    GROUP BY product_id
)
SELECT
    p.category,
    ir.revenue
FROM item_rev ir
JOIN products p
    ON ir.product_id = p.product_id
ORDER BY ir.revenue DESC;
