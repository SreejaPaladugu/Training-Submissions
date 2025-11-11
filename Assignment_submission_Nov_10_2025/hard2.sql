-- Hard 2: Build a mini project applying SQL Basics end-to-end.

-- Create Customers table
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    country TEXT
);

-- Create Products table
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price DECIMAL(10,2)
);

-- Create Orders table
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
-- Insert Customers
INSERT INTO Customers VALUES
(1, 'Sreeja', 'Charlotte', 'USA'),
(2, 'Anil', 'Mumbai', 'India'),
(3, 'Emma', 'Toronto', 'Canada'),
(4, 'Marcus', 'New York', 'USA'),
(5, 'Priya', 'Bangalore', 'India');

-- Insert Products
INSERT INTO Products VALUES
(101, 'Laptop', 'Electronics', 950.00),
(102, 'Headphones', 'Electronics', 120.00),
(103, 'Desk Chair', 'Furniture', 180.00),
(104, 'Notebook', 'Stationery', 5.00),
(105, 'Coffee Mug', 'Kitchen', 12.00);

-- Insert Orders
INSERT INTO Orders VALUES
(1001, 1, 101, 1, '2024-09-10'),
(1002, 2, 105, 2, '2024-09-11'),
(1003, 3, 103, 1, '2024-09-13'),
(1004, 1, 102, 1, '2024-09-15'),
(1005, 4, 104, 5, '2024-09-18'),
(1006, 5, 101, 1, '2024-09-20'),
(1007, 3, 105, 3, '2024-09-21'),
(1008, 2, 103, 2, '2024-09-22'),
(1009, 4, 102, 2, '2024-09-25'),
(1010, 5, 104, 4, '2024-09-27');
-- Join tables to view all order details
SELECT o.order_id, c.name AS customer, p.product_name,
       o.quantity, p.price,
       (o.quantity * p.price) AS total_amount, o.order_date
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Products p ON o.product_id = p.product_id
ORDER BY o.order_date;

-- Total revenue
SELECT SUM(o.quantity * p.price) AS total_revenue
FROM Orders o
JOIN Products p ON o.product_id = p.product_id;

-- Revenue by country
SELECT c.country, SUM(o.quantity * p.price) AS revenue
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Products p ON o.product_id = p.product_id
GROUP BY c.country
ORDER BY revenue DESC;

-- Top-selling products
SELECT p.product_name, SUM(o.quantity) AS total_sold
FROM Orders o
JOIN Products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sold DESC
LIMIT 3;

-- Most valuable customers
SELECT c.name, SUM(o.quantity * p.price) AS total_spent
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Products p ON o.product_id = p.product_id
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 3;

-- Category-wise revenue
SELECT p.category, SUM(o.quantity * p.price) AS category_revenue
FROM Orders o
JOIN Products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;
