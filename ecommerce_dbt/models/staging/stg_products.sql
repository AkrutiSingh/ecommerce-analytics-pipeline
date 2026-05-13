WITH source AS (
    SELECT * FROM {{ source('raw', 'PRODUCTS') }}
),

renamed AS (
    SELECT
        PRODUCT_ID                  AS product_id,
        PRODUCT_CATEGORY_NAME       AS product_category_name,
        TRY_CAST(PRODUCT_WEIGHT_G AS FLOAT)    AS product_weight_g,
        TRY_CAST(PRODUCT_LENGTH_CM AS FLOAT)   AS product_length_cm,
        TRY_CAST(PRODUCT_HEIGHT_CM AS FLOAT)   AS product_height_cm,
        TRY_CAST(PRODUCT_WIDTH_CM AS FLOAT)    AS product_width_cm
    FROM source
)

SELECT * FROM renamed