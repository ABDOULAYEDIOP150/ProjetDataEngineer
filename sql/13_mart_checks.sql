SELECT COUNT(*) AS total_dim_customers
FROM mart.dim_customers;

SELECT COUNT(*) AS total_dim_products
FROM mart.dim_products;

SELECT COUNT(*) AS total_dim_date
FROM mart.dim_date;

SELECT COUNT(*) AS total_fact_sales
FROM mart.fact_sales;

SELECT COUNT(*) AS total_fact_payments
FROM mart.fact_payments;

SELECT *
FROM mart.v_sales_by_month
LIMIT 10;

SELECT *
FROM mart.v_top_products
LIMIT 10;

SELECT *
FROM mart.v_customer_revenue
LIMIT 10;