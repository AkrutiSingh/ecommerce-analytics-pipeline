WITH order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

orders AS (
    -- Only delivered orders
    SELECT order_id FROM {{ ref('stg_orders') }}
    WHERE order_status = 'delivered'
)

SELECT
    COALESCE(p.product_category_name, 'unknown')    AS category,
    COUNT(DISTINCT oi.order_id)                     AS total_orders,
    COUNT(oi.product_id)                            AS total_items_sold,
    ROUND(SUM(oi.price), 2)                         AS total_revenue,
    ROUND(AVG(oi.price), 2)                         AS avg_price

FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
INNER JOIN orders o  ON oi.order_id   = o.order_id
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 20