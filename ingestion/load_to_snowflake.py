import snowflake.connector
import pandas as pd
import numpy as np
import os

# ── Connection ──────────────────────────────────────────
conn = snowflake.connector.connect(
    user='Akruti1301',
    password='Akrutisingh1313',
    account='ZXVHNYA-BN15688',
    warehouse='ECOMMERCE_WH',
    database='ECOMMERCE_DB',
    schema='RAW'
)
cursor = conn.cursor()
print("✅ Connected to Snowflake!")

# ── Folder where your CSV files are ─────────────────────
DATA_FOLDER = r"C:\Users\user\Downloads\projjj"

# ── CSV files to load ────────────────────────────────────
csv_files = {
    'ORDERS':               'olist_orders_dataset.csv',
    'CUSTOMERS':            'olist_customers_dataset.csv',
    'ORDER_ITEMS':          'olist_order_items_dataset.csv',
    'PRODUCTS':             'olist_products_dataset.csv',
    'SELLERS':              'olist_sellers_dataset.csv',
    'ORDER_PAYMENTS':       'olist_order_payments_dataset.csv',
    'ORDER_REVIEWS':        'olist_order_reviews_dataset.csv',
    'GEOLOCATION':          'olist_geolocation_dataset.csv',
    'CATEGORY_TRANSLATION': 'product_category_name_translation.csv',
}

# ── Helper: convert pandas dtype to Snowflake type ───────
def get_sf_type(dtype):
    if 'int' in str(dtype):
        return 'NUMBER'
    elif 'float' in str(dtype):
        return 'FLOAT'
    else:
        return 'VARCHAR(500)'

# ── Helper: clean a single value ─────────────────────────
def clean_val(val):
    if val is None:
        return None
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str) and val.strip().lower() in ('nan', 'none', 'null', ''):
        return None
    return val

# ── Load each CSV ─────────────────────────────────────────
for table_name, filename in csv_files.items():
    filepath = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(filepath):
        print(f"⚠️  File not found, skipping: {filename}")
        continue

    print(f"\n📂 Loading {filename} → RAW.{table_name}")

    # Read CSV — treat empty strings as NaN
    df = pd.read_csv(filepath, keep_default_na=True)
    df.columns = [col.upper() for col in df.columns]
    print(f"   Rows: {len(df):,}  |  Columns: {len(df.columns)}")

    # Drop table if exists and recreate
    cursor.execute(f"DROP TABLE IF EXISTS ECOMMERCE_DB.RAW.{table_name}")

    # Build CREATE TABLE — all columns as VARCHAR to avoid type issues
    col_defs = ", ".join([f"{col} VARCHAR(500)" for col in df.columns])
    cursor.execute(f"CREATE TABLE ECOMMERCE_DB.RAW.{table_name} ({col_defs})")
    print(f"   ✅ Table created")

    # Convert entire dataframe to string, replace NaN with None
    df = df.astype(object).where(pd.notnull(df), None)

    # Insert data in batches of 5000 rows
    batch_size = 5000
    total_batches = (len(df) // batch_size) + 1

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i + batch_size]
        rows = [
            tuple(clean_val(v) for v in row)
            for row in batch.itertuples(index=False)
        ]
        placeholders = ", ".join(["%s"] * len(df.columns))
        cursor.executemany(
            f"INSERT INTO ECOMMERCE_DB.RAW.{table_name} VALUES ({placeholders})",
            rows
        )
        print(f"   Batch {(i // batch_size) + 1}/{total_batches} loaded...", end='\r')

    print(f"   ✅ All {len(df):,} rows loaded into RAW.{table_name}    ")

# ── Done ──────────────────────────────────────────────────
print("\n🎉 All tables loaded successfully into Snowflake RAW schema!")
cursor.close()
conn.close()