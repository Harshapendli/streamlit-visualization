import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Business & Data Quality Insights", layout="wide")

st.title("📊 Business & Data Quality Dashboard")

# Replace with actual GitHub raw URLs
data_sources = {
    "business_metrics": "https://raw.githubusercontent.com/Harshapendli/streamlit-visualization/main/incorrect_products.csv",
    "data_quality": "https://raw.githubusercontent.com/Harshapendli/streamlit-visualization/main/incorrect_products.csv"
}

@st.cache_data
def load_csv(url):
    return pd.read_csv(url, engine='python', on_bad_lines='warn')

# Load datasets
biz_df = load_csv(data_sources["business_metrics"])
dq_df = load_csv(data_sources["data_quality"])

# Convert date if available
if 'date' in biz_df.columns:
    biz_df['date'] = pd.to_datetime(biz_df['date'], errors='coerce')

st.header("📊 Business Insights Report")

# Top 5 Customers
st.subheader("🏅 Top 5 Customers by Total Spend")
if 'customer_name' in biz_df.columns:
    top_customers = biz_df.groupby(['customer_id', 'customer_name'])['total_spent'].sum().nlargest(5).reset_index()
    st.dataframe(top_customers)
    fig_cust = px.bar(top_customers, x='customer_name', y='total_spent', color='customer_name')
    st.plotly_chart(fig_cust, use_container_width=True)

# Top 5 Products
st.subheader("🛍️ Top 5 Products by Revenue")
if 'product_name' in biz_df.columns:
    top_products = biz_df.groupby(['product_id', 'product_name'])['total_revenue'].sum().nlargest(5).reset_index()
    st.dataframe(top_products)
    fig_prod = px.bar(top_products, x='product_name', y='total_revenue', color='product_name')
    st.plotly_chart(fig_prod, use_container_width=True)

# Shipping Performance
st.subheader("🚚 Top 5 Shipping Carriers by On-Time Deliveries")
if 'carrier' in biz_df.columns:
    shipping = biz_df.groupby('carrier')['on_time_deliveries'].sum().nlargest(5).reset_index()
    st.dataframe(shipping)
    fig_ship = px.bar(shipping, x='carrier', y='on_time_deliveries', color='carrier')
    st.plotly_chart(fig_ship, use_container_width=True)

# Refund Reasons
st.subheader("💸 Top 5 Return Reasons")
if 'reason' in biz_df.columns:
    refunds = biz_df.groupby('reason')['total_refund_amount'].sum().nlargest(5).reset_index()
    st.dataframe(refunds)
    fig_ref = px.pie(refunds, names='reason', values='total_refund_amount', title='Top Refund Reasons')
    st.plotly_chart(fig_ref, use_container_width=True)

st.header("🧮 Data Quality Report")

# Invalid records by dataset
st.subheader("📦 Invalid Record Counts")
if not dq_df.empty:
    st.dataframe(dq_df)
    fig_dq = px.bar(dq_df, x='dataset', y='invalid_count', color='dataset', title="Invalid Records per Dataset")
    st.plotly_chart(fig_dq, use_container_width=True)

# Summarized issues
st.subheader("🔍 Issue Summary by Type")
if 'issue_type' in dq_df.columns:
    issue_summary = dq_df.groupby('issue_type')['invalid_count'].sum().reset_index()
    fig_issues = px.bar(issue_summary, x='issue_type', y='invalid_count', color='issue_type', title='Summarized Issues by Type')
    st.plotly_chart(fig_issues, use_container_width=True)

# Bonus Dashboard
st.header("📈 Interactive Dashboard")
if 'date' in biz_df.columns:
    st.subheader("📅 Filter by Date Range")
    min_date = biz_df['date'].min()
    max_date = biz_df['date'].max()
    date_range = st.date_input("Select date range", [min_date, max_date])

    if len(date_range) == 2:
        filtered = biz_df[(biz_df['date'] >= pd.to_datetime(date_range[0])) & (biz_df['date'] <= pd.to_datetime(date_range[1]))]

        st.subheader("📊 Spend Over Time")
        if not filtered.empty:
            spend_time = filtered.groupby('date')['total_spent'].sum().reset_index()
            fig_spend = px.line(spend_time, x='date', y='total_spent', title='Total Spend Over Time')
            st.plotly_chart(fig_spend, use_container_width=True)

        st.subheader("📦 Shipping Performance Over Time")
        if 'on_time_deliveries' in filtered.columns:
            ship_time = filtered.groupby('date')['on_time_deliveries'].sum().reset_index()
            fig_ship_time = px.line(ship_time, x='date', y='on_time_deliveries', title='On-Time Deliveries Over Time')
            st.plotly_chart(fig_ship_time, use_container_width=True)

        st.subheader("💰 Refund Amounts Over Time")
        if 'total_refund_amount' in filtered.columns:
            refund_time = filtered.groupby('date')['total_refund_amount'].sum().reset_index()
            fig_refund_time = px.line(refund_time, x='date', y='total_refund_amount', title='Refunds Over Time')
            st.plotly_chart(fig_refund_time, use_container_width=True)
    else:
        st.warning("Please select a valid date range.")
