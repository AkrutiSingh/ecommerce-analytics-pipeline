# 🛒 End-to-End E-Commerce Analytics Pipeline

> A production-grade data engineering portfolio project built using the modern data stack — Python, Snowflake, dbt, and Streamlit.

---

## 📌 Project Overview

This project builds a complete data pipeline for the **Olist Brazilian E-Commerce dataset** — from raw CSV files to a live analytics dashboard.

It simulates exactly what data engineers do at MNCs:
- Ingest raw data into a cloud data warehouse
- Transform and model data using dbt (Bronze → Silver → Gold)
- Enforce data quality with automated tests
- Deliver business insights via an interactive dashboard

---

## 🏗️ Architecture

```
CSV Files (9 files)
       |
       | Python + pandas
       v
Snowflake RAW Schema        [Bronze Layer]
9 tables, 1.4M rows
       |
       | dbt staging models
       v
Snowflake STAGING Schema    [Silver Layer]
cleaned, typed, renamed
       |
       | dbt marts models
       v
Snowflake MARTS Schema      [Gold Layer]
joined, aggregated
       |
       | Streamlit + Plotly
       v
Live Analytics Dashboard
```

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Data ingestion, pipeline scripting |
| Snowflake | - | Cloud data warehouse |
| dbt | 1.11 | Data transformation + testing + docs |
| Streamlit | Latest | Interactive dashboard |
| Plotly | Latest | Charts and visualizations |
| pandas | Latest | CSV reading and data manipulation |
| Git + GitHub | - | Version control |

---

## 📁 Project Structure

ecommerce-pipeline/
│
├── .env.example                    # Credential template (never commit .env)
├── .gitignore                      # Protects credentials and venv
├── requirements.txt                # Python dependencies
├── README.md                       # You are here!
│
├── ingestion/
│   ├── load_to_snowflake.py        # Loads 9 CSV files → Snowflake RAW
│   └── test_connection.py          # Verifies Snowflake connectivity
│
├── ecommerce_dbt/
│   ├── dbt_project.yml             # dbt project configuration
│   └── models/
│       ├── staging/                # Silver layer — 5 cleaning models
│       │   ├── sources.yml         # Source definitions + tests
│       │   ├── stg_orders.sql
│       │   ├── stg_customers.sql
│       │   ├── stg_order_items.sql
│       │   ├── stg_products.sql
│       │   └── stg_order_payments.sql
│       └── marts/                  # Gold layer — 3 business models
│           ├── schema.yml          # Model documentation + tests
│           ├── fct_orders.sql      # Core fact table (99,441 rows)
│           ├── monthly_revenue.sql # Revenue trends by month
│           └── top_products.sql    # Top 20 product categories
│
└── dashboard/
└── app.py                      # Streamlit dashboard (5 charts)

![ss1](../Streamlit1.png)
![ss2](../Streamlit2.png)
![ss3](../Streamlit3.png)
![ss4](../Streamlit4.png)
![ss5](../Streamlit5.png)
![ss6](../Streamlit6.png)

## 🔍 dbt Lineage Graph

![lg1](<../Lineage Graph.png>)

> The lineage graph shows how data flows from RAW sources → staging models → marts models. Built automatically by dbt docs.

## 📈 Key Business Insights

| Metric | Value |
|--------|-------|
| Total Orders | 99,441 |
| Total Revenue | R$ 13.6M+ |
| Date Range | Jan 2017 – Aug 2018 |
| Top Category | Health & Beauty |
| Avg Delivery Time | ~12 days |
| Total Customers | 96,096 |

---

## 🗄️ Data Models

### Staging Layer (Silver)
| Model | Source | Description |
|-------|--------|-------------|
| stg_orders | RAW.ORDERS | Cleaned orders with proper timestamps |
| stg_customers | RAW.CUSTOMERS | Customer details with city/state |
| stg_order_items | RAW.ORDER_ITEMS | Items with price cast to FLOAT |
| stg_products | RAW.PRODUCTS | Products with category names |
| stg_order_payments | RAW.ORDER_PAYMENTS | Payments cast to proper types |

### Marts Layer (Gold)
| Model | Rows | Description |
|-------|------|-------------|
| fct_orders | 99,441 | Master fact table — orders joined with customers, payments, items |
| monthly_revenue | 23 | Monthly revenue, orders, customers, delivery metrics |
| top_products | 20 | Top 20 categories by revenue |

---

## ✅ Data Quality Tests

25 automated dbt tests — all passing ✅

Source Tests (RAW layer):
✅ orders.order_id          → unique, not_null
✅ customers.customer_id    → unique, not_null
✅ products.product_id      → unique, not_null
✅ sellers.seller_id        → unique, not_null
✅ order_items.order_id     → not_null
✅ order_items.price        → not_null
✅ order_payments.order_id  → not_null
✅ order_reviews.order_id   → not_null
Model Tests (Gold layer):
✅ fct_orders.order_id           → unique, not_null
✅ fct_orders.customer_id        → not_null
✅ fct_orders.order_status       → not_null
✅ monthly_revenue.order_month   → unique, not_null
✅ monthly_revenue.total_revenue → not_null
✅ top_products.category         → unique, not_null
✅ top_products.total_revenue    → not_null

---

## 🚀 How to Run This Project

### Prerequisites
- Python 3.11+
- Snowflake free trial account
- Git

### 1. Clone the repository
```bash
git clone https://github.com/AkrutiSingh/ecommerce-analytics-pipeline.git
cd ecommerce-analytics-pipeline
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure credentials
```bash
cp .env.example .env
# Open .env and fill in your Snowflake credentials
```

### 5. Setup Snowflake
Run this SQL in your Snowflake worksheet:
```sql
CREATE DATABASE ECOMMERCE_DB;
CREATE SCHEMA ECOMMERCE_DB.RAW;
CREATE SCHEMA ECOMMERCE_DB.STAGING;
CREATE SCHEMA ECOMMERCE_DB.MARTS;
CREATE WAREHOUSE ECOMMERCE_WH
  WITH WAREHOUSE_SIZE = 'X-SMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;
```

### 6. Download dataset
Download [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle and update the `DATA_FOLDER` path in `ingestion/load_to_snowflake.py`.

### 7. Load raw data
```bash
python ingestion/load_to_snowflake.py
```

### 8. Run dbt models
```bash
cd ecommerce_dbt
dbt run
dbt test
dbt docs generate
dbt docs serve  # Opens docs at localhost:8080
```

### 9. Launch dashboard
```bash
cd ..
streamlit run dashboard/app.py
# Opens at localhost:8501
```

---

## 💡 What I Learned

- Designing a **3-layer data warehouse** (Bronze/Silver/Gold) in Snowflake
- Building **production-grade dbt models** with tests and documentation
- Writing **optimized SQL** with CTEs, window functions, and aggregations
- Implementing **data quality testing** as part of the pipeline
- Managing **credentials securely** using environment variables
- Building an **interactive dashboard** connecting directly to Snowflake

---

## 🔮 Future Improvements

- [ ] Add Apache Airflow DAG for daily pipeline orchestration
- [ ] Add real-time streaming with Kafka CDC simulation
- [ ] Add Great Expectations for advanced data quality checks
- [ ] Deploy Streamlit dashboard to Streamlit Cloud (free)
- [ ] Add seller performance and customer cohort analysis models

---

## 👩‍💻 Author

**Akruti Singh**
- LinkedIn: [linkedin.com/in/akrutisingh](https://linkedin.com/in/akrutisingh)
- GitHub: [github.com/AkrutiSingh](https://github.com/AkrutiSingh)
- Email: akrutisingh1301@gmail.com

---

*Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — Kaggle*