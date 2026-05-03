-- =====================================================
-- 15 - WINDOW FUNCTIONS
-- =====================================================

-- 1. Classement des clients par chiffre d'affaires

SELECT
    c.customer_id,
    c.full_name,
    SUM(f.line_total) AS total_revenue,
    RANK() OVER (ORDER BY SUM(f.line_total) DESC) AS revenue_rank
FROM mart.fact_sales f
JOIN mart.dim_customers c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.full_name
ORDER BY revenue_rank;


-- 2. Classement des produits par catégorie

SELECT
    p.category,
    p.product_name,
    SUM(f.line_total) AS total_revenue,
    RANK() OVER (
        PARTITION BY p.category
        ORDER BY SUM(f.line_total) DESC
    ) AS rank_in_category
FROM mart.fact_sales f
JOIN mart.dim_products p
    ON f.product_id = p.product_id
GROUP BY
    p.category,
    p.product_name
ORDER BY
    p.category,
    rank_in_category;


-- 3. Évolution du chiffre d'affaires mensuel avec LAG

WITH monthly_sales AS (
    SELECT
        d.year,
        d.month,
        SUM(f.line_total) AS monthly_revenue
    FROM mart.fact_sales f
    JOIN mart.dim_date d
        ON f.order_date = d.date_id
    GROUP BY
        d.year,
        d.month
)
SELECT
    year,
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (
        ORDER BY year, month
    ) AS previous_month_revenue,
    monthly_revenue - LAG(monthly_revenue) OVER (
        ORDER BY year, month
    ) AS revenue_difference
FROM monthly_sales
ORDER BY
    year,
    month;


-- 4. Chiffre d'affaires cumulé

WITH monthly_sales AS (
    SELECT
        d.year,
        d.month,
        SUM(f.line_total) AS monthly_revenue
    FROM mart.fact_sales f
    JOIN mart.dim_date d
        ON f.order_date = d.date_id
    GROUP BY
        d.year,
        d.month
)
SELECT
    year,
    month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (
        ORDER BY year, month
    ) AS cumulative_revenue
FROM monthly_sales
ORDER BY
    year,
    month;