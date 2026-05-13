WITH source AS (
    SELECT * FROM {{ source('raw', 'CUSTOMERS') }}
),

renamed AS (
    SELECT
        CUSTOMER_ID             AS customer_id,
        CUSTOMER_UNIQUE_ID      AS customer_unique_id,
        CUSTOMER_ZIP_CODE_PREFIX AS customer_zip_code,
        CUSTOMER_CITY           AS customer_city,
        CUSTOMER_STATE          AS customer_state
    FROM source
)

SELECT * FROM renamed