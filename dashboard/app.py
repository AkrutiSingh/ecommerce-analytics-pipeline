import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# ── Snowflake Connection ─────────────────────────────────
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema='STAGING'
    )

# ── Load Data ────────────────────────────────────────────
@st.cache_data
def load_monthly_revenue():
    conn = get_connection()
    query = """
        SELECT
            ORDER_MONTH,
            TOTAL_ORDERS,
            UNIQUE_CUSTOMERS,
            TOTAL_REVENUE,
            AVG_ORDER_VALUE,
            AVG_DELIVERY_DAYS
        FROM ECOMMERCE_DB.STAGING.MONTHLY_REVENUE
        ORDER BY ORDER_MONTH
    """
    return pd.read_sql(query, conn)

@st.cache_data
def load_top_products():
    conn = get_connection()
    query = """
        SELECT
            CATEGORY,
            TOTAL_ORDERS,
            TOTAL_ITEMS_SOLD,
            TOTAL_REVENUE,
            AVG_PRICE
        FROM ECOMMERCE_DB.STAGING.TOP_PRODUCTS
        ORDER BY TOTAL_REVENUE DESC
    """
    return pd.read_sql(query, conn)

@st.cache_data
def load_order_status():
    conn = get_connection()
    query = """
        SELECT
            ORDER_STATUS,
            COUNT(*) AS total_orders
        FROM ECOMMERCE_DB.STAGING.FCT_ORDERS
        GROUP BY ORDER_STATUS
        ORDER BY total_orders DESC
    """
    return pd.read_sql(query, conn)

@st.cache_data
def load_kpis():
    conn = get_connection()
    query = """
        SELECT
            COUNT(DISTINCT ORDER_ID)        AS total_orders,
            COUNT(DISTINCT CUSTOMER_ID)     AS total_customers,
            ROUND(SUM(TOTAL_PAYMENT_VALUE), 2) AS total_revenue,
            ROUND(AVG(DELIVERY_DAYS), 1)    AS avg_delivery_days
        FROM ECOMMERCE_DB.STAGING.FCT_ORDERS
        WHERE ORDER_STATUS = 'delivered'
    """
    return pd.read_sql(query, conn)

# ── Dashboard ────────────────────────────────────────────
st.title("🛒 Olist E-Commerce Analytics Dashboard")
st.markdown("Built with **dbt + Snowflake + Streamlit** | Data Engineer Portfolio Project")
st.divider()

# Load all data
monthly_df    = load_monthly_revenue()
products_df   = load_top_products()
status_df     = load_order_status()
kpis_df       = load_kpis()

# ── KPI Cards ────────────────────────────────────────────
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Revenue",
        value=f"R$ {kpis_df['TOTAL_REVENUE'].iloc[0]:,.0f}"
    )
with col2:
    st.metric(
        label="Total Orders",
        value=f"{kpis_df['TOTAL_ORDERS'].iloc[0]:,}"
    )
with col3:
    st.metric(
        label="Total Customers",
        value=f"{kpis_df['TOTAL_CUSTOMERS'].iloc[0]:,}"
    )
with col4:
    st.metric(
        label="Avg Delivery Days",
        value=f"{kpis_df['AVG_DELIVERY_DAYS'].iloc[0]} days"
    )

st.divider()

# ── Revenue Trend ────────────────────────────────────────
st.subheader("📈 Monthly Revenue Trend")
fig_revenue = px.line(
    monthly_df,
    x='ORDER_MONTH',
    y='TOTAL_REVENUE',
    title='Monthly Revenue (Delivered Orders)',
    labels={'ORDER_MONTH': 'Month', 'TOTAL_REVENUE': 'Revenue (R$)'},
    markers=True,
    color_discrete_sequence=['#2471A3']
)
fig_revenue.update_layout(hovermode='x unified')
st.plotly_chart(fig_revenue, use_container_width=True)

# ── Two columns ──────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 Top 10 Product Categories")
    fig_products = px.bar(
        products_df.head(10),
        x='TOTAL_REVENUE',
        y='CATEGORY',
        orientation='h',
        title='Revenue by Product Category',
        labels={'TOTAL_REVENUE': 'Revenue (R$)', 'CATEGORY': 'Category'},
        color='TOTAL_REVENUE',
        color_continuous_scale='Blues'
    )
    fig_products.update_layout(showlegend=False)
    st.plotly_chart(fig_products, use_container_width=True)

with col_right:
    st.subheader("📦 Order Status Breakdown")
    fig_status = px.pie(
        status_df,
        values='TOTAL_ORDERS',
        names='ORDER_STATUS',
        title='Orders by Status',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    st.plotly_chart(fig_status, use_container_width=True)

st.divider()

# ── Monthly Orders + Customers ───────────────────────────
st.subheader("👥 Monthly Orders vs Customers")
fig_orders = px.bar(
    monthly_df,
    x='ORDER_MONTH',
    y=['TOTAL_ORDERS', 'UNIQUE_CUSTOMERS'],
    title='Monthly Orders and Unique Customers',
    labels={'ORDER_MONTH': 'Month', 'value': 'Count'},
    barmode='group',
    color_discrete_sequence=['#2471A3', '#85C1E9']
)
st.plotly_chart(fig_orders, use_container_width=True)

# ── Avg Delivery Days ────────────────────────────────────
st.subheader("🚚 Average Delivery Days by Month")
fig_delivery = px.line(
    monthly_df,
    x='ORDER_MONTH',
    y='AVG_DELIVERY_DAYS',
    title='Average Delivery Time (Days)',
    labels={'ORDER_MONTH': 'Month', 'AVG_DELIVERY_DAYS': 'Avg Days'},
    markers=True,
    color_discrete_sequence=['#E74C3C']
)
st.plotly_chart(fig_delivery, use_container_width=True)

st.divider()
st.markdown("*Data Source: Olist Brazilian E-Commerce Dataset | Pipeline: Python → Snowflake → dbt → Streamlit*")