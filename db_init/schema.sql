CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    vendor_id INT REFERENCES vendors(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    total NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    amount NUMERIC NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO vendors (name) VALUES ('Amazon'), ('Walmart');

INSERT INTO products (name, price, vendor_id) VALUES
('Laptop', 699.99, 1),
('Phone', 399.99, 2);
