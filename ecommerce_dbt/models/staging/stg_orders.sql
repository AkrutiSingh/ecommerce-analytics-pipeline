WITH source AS (
    SELECT * FROM {{ source('raw', 'ORDERS') }}
),

renamed AS (
    SELECT
        ORDER_ID                                    AS order_id,
        CUSTOMER_ID                                 AS customer_id,
        ORDER_STATUS                                AS order_status,
        TO_TIMESTAMP(ORDER_PURCHASE_TIMESTAMP)      AS order_purchased_at,
        TO_TIMESTAMP(ORDER_APPROVED_AT)             AS order_approved_at,
        TO_TIMESTAMP(ORDER_DELIVERED_CARRIER_DATE)  AS order_delivered_carrier_at,
        TO_TIMESTAMP(ORDER_DELIVERED_CUSTOMER_DATE) AS order_delivered_customer_at,
        TO_TIMESTAMP(ORDER_ESTIMATED_DELIVERY_DATE) AS order_estimated_delivery_at
    FROM source
)

SELECT * FROM renamed