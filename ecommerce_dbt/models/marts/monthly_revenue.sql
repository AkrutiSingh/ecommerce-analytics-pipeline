WITH fct AS (
    SELECT * FROM {{ ref('fct_orders') }}
)

SELECT
    order_month,
    COUNT(DISTINCT order_id)                        AS total_orders,
    COUNT(DISTINCT customer_id)                     AS unique_customers,
    ROUND(COALESCE(SUM(total_payment_value), 0), 2) AS total_revenue,
    ROUND(COALESCE(AVG(total_payment_value), 0), 2) AS avg_order_value,
    ROUND(COALESCE(AVG(delivery_days), 0), 1)       AS avg_delivery_days

FROM fct
WHERE order_status = 'delivered'
  AND order_month IS NOT NULL
  AND total_payment_value IS NOT NULL        -- exclude orders with no payment
GROUP BY order_month
ORDER BY order_month