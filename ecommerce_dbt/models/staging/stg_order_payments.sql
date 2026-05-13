WITH source AS (
    SELECT * FROM {{ source('raw', 'ORDER_PAYMENTS') }}
),

renamed AS (
    SELECT
        ORDER_ID                            AS order_id,
        TRY_CAST(PAYMENT_SEQUENTIAL AS INT) AS payment_sequential,
        PAYMENT_TYPE                        AS payment_type,
        TRY_CAST(PAYMENT_INSTALLMENTS AS INT) AS payment_installments,
        TRY_CAST(PAYMENT_VALUE AS FLOAT)    AS payment_value
    FROM source
)

SELECT * FROM renamed