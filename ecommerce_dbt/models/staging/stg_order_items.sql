WITH source AS (
    SELECT * FROM {{ source('raw', 'ORDER_ITEMS') }}
),

renamed AS (
    SELECT
        ORDER_ID                            AS order_id,
        ORDER_ITEM_ID                       AS order_item_id,
        PRODUCT_ID                          AS product_id,
        SELLER_ID                           AS seller_id,
        TO_TIMESTAMP(SHIPPING_LIMIT_DATE)   AS shipping_limit_at,
        TRY_CAST(PRICE AS FLOAT)            AS price,
        TRY_CAST(FREIGHT_VALUE AS FLOAT)    AS freight_value
    FROM source
)

SELECT * FROM renamed