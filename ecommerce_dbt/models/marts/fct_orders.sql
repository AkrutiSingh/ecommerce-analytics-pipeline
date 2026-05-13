WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

payments AS (
    -- Total payment per order (one order can have multiple payments)
    SELECT
        order_id,
        SUM(payment_value)  AS total_payment_value,
        COUNT(*)            AS payment_count
    FROM {{ ref('stg_order_payments') }}
    GROUP BY order_id
),

order_items AS (
    -- Total items and freight per order
    SELECT
        order_id,
        COUNT(*)                    AS total_items,
        SUM(price)                  AS total_price,
        SUM(freight_value)          AS total_freight
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
)

SELECT
    -- Order details
    o.order_id,
    o.order_status,
    o.order_purchased_at,
    DATE_TRUNC('month', o.order_purchased_at)   AS order_month,
    DATE_TRUNC('year',  o.order_purchased_at)   AS order_year,

    -- Customer details
    c.customer_id,
    c.customer_city,
    c.customer_state,

    -- Revenue details
    oi.total_items,
    oi.total_price,
    oi.total_freight,
    p.total_payment_value,

    -- Delivery time in days
    DATEDIFF('day',
        o.order_purchased_at,
        o.order_delivered_customer_at
    ) AS delivery_days

FROM orders o
LEFT JOIN customers      c  ON o.customer_id  = c.customer_id
LEFT JOIN payments       p  ON o.order_id     = p.order_id
LEFT JOIN order_items    oi ON o.order_id     = oi.order_id