CREATE OR REPLACE VIEW mart.v_sales_by_month AS
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.line_total) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM mart.fact_sales f
JOIN mart.dim_date d
    ON f.order_date = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;

CREATE OR REPLACE VIEW mart.v_top_products AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.line_total) AS total_revenue
FROM mart.fact_sales f
JOIN mart.dim_products p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_revenue DESC;

CREATE OR REPLACE VIEW mart.v_customer_revenue AS
SELECT
    c.customer_id,
    c.full_name,
    c.city,
    c.country,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.line_total) AS total_revenue
FROM mart.fact_sales f
JOIN mart.dim_customers c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.full_name,
    c.city,
    c.country
ORDER BY total_revenue DESC;