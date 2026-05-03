DROP TABLE IF EXISTS mart.fact_payments;
DROP TABLE IF EXISTS mart.fact_sales;
DROP TABLE IF EXISTS mart.dim_date;
DROP TABLE IF EXISTS mart.dim_products;
DROP TABLE IF EXISTS mart.dim_customers;

CREATE TABLE mart.dim_customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    city TEXT,
    country TEXT,
    created_at TIMESTAMP
);

CREATE TABLE mart.dim_products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(10,2),
    created_at TIMESTAMP
);

CREATE TABLE mart.dim_date (
    date_id DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    month_name TEXT,
    quarter INTEGER
);

CREATE TABLE mart.fact_sales (
    sales_id SERIAL PRIMARY KEY,
    order_id INTEGER,
    order_item_id INTEGER,
    customer_id INTEGER REFERENCES mart.dim_customers(customer_id),
    product_id INTEGER REFERENCES mart.dim_products(product_id),
    order_date DATE REFERENCES mart.dim_date(date_id),
    status TEXT,
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    line_total NUMERIC(10,2)
);

CREATE TABLE mart.fact_payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    customer_id INTEGER REFERENCES mart.dim_customers(customer_id),
    payment_date DATE REFERENCES mart.dim_date(date_id),
    payment_method TEXT,
    payment_status TEXT,
    amount NUMERIC(10,2)
);