CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    country TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(10,2) CHECK (price >= 0),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES staging.customers(customer_id),
    order_date TIMESTAMP,
    status TEXT CHECK (status IN ('delivered', 'shipped', 'processing', 'cancelled'))
);

CREATE TABLE IF NOT EXISTS staging.order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES staging.orders(order_id),
    product_id INTEGER REFERENCES staging.products(product_id),
    quantity INTEGER CHECK (quantity > 0),
    unit_price NUMERIC(10,2),
    line_total NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS staging.payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES staging.orders(order_id),
    payment_method TEXT,
    amount NUMERIC(10,2),
    payment_date TIMESTAMP,
    payment_status TEXT
);