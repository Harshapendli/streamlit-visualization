import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Product Data Quality Dashboard", layout="wide")

st.title("📊 Business Insights & Product Data Quality Dashboard")

# ✅ Raw GitHub CSV URLs
PRODUCTS_CSV_URL = "https://raw.githubusercontent.com/Harshapendli/streamlit-visualization/main/incorrect_products.csv"
BUSINESS_METRICS_URL = "https://raw.githubusercontent.com/Harshapendli/streamlit-visualization/main/business_metrics.csv"

@st.cache_data
def load_data(url):
    try:
        return pd.read_csv(url, engine='python', on_bad_lines='warn')
    except Exception as e:
        st.stop()
        st.error(f"Error reading CSV: {e}")

# Load datasets
product_df = load_data(PRODUCTS_CSV_URL)
biz_df = load_data(BUSINESS_METRICS_URL)

st.subheader("🧾 Raw Product Data Preview")
st.dataframe(product_df)

# ---------- Business Insights Report ----------
st.header("📊 Business Insights Report")

# Top 5 Customers by Total Spend
if {'customer_id', 'customer_name', 'total_spent'}.issubset(biz_df.columns):
    st.subheader("🏅 Top 5 Customers by Total Spend")
    top_customers = biz_df.groupby(['customer_id', 'customer_name'])['total_spent'].sum().nlargest(5).reset_index()
    st.dataframe(top_customers)
    fig = px.bar(top_customers, x='customer_name', y='total_spent', color='customer_name', title="Top 5 Customers")
    st.plotly_chart(fig, use_container_width=True)

# Top 5 Products by Revenue
if {'product_id', 'product_name', 'total_revenue'}.issubset(biz_df.columns):
    st.subheader("🛍️ Top 5 Products by Revenue")
    top_products = biz_df.groupby(['product_id', 'product_name'])['total_revenue'].sum().nlargest(5).reset_index()
    st.dataframe(top_products)
    fig = px.bar(top_products, x='product_name', y='total_revenue', color='product_name', title="Top 5 Products")
    st.plotly_chart(fig, use_container_width=True)

# Top 5 Shipping Carriers by On-Time Deliveries
if {'carrier', 'on_time_deliveries'}.issubset(biz_df.columns):
    st.subheader("🚚 Top 5 Shipping Carriers by On-Time Deliveries")
    top_carriers = biz_df.groupby('carrier')['on_time_deliveries'].sum().nlargest(5).reset_index()
    st.dataframe(top_carriers)
    fig = px.bar(top_carriers, x='carrier', y='on_time_deliveries', color='carrier', title="Top Shipping Carriers")
    st.plotly_chart(fig, use_container_width=True)

# Top 5 Refund Reasons
if {'reason', 'total_refund_amount'}.issubset(biz_df.columns):
    st.subheader("💸 Top 5 Return Reason Analysis")
    refund_reasons = biz_df.groupby('reason')['total_refund_amount'].sum().nlargest(5).reset_index()
    st.dataframe(refund_reasons)
    fig = px.pie(refund_reasons, names='reason', values='total_refund_amount', title="Top Refund Reasons")
    st.plotly_chart(fig, use_container_width=True)

# ---------- Product Data Quality Analysis ----------
st.header("🧮 Product Data Quality Report")

product_df['category'] = product_df['category'].astype(str).str.strip()
total_rows = len(product_df)

# Validation Issue Count
st.subheader("❗ Frequent Validation Issues")
val_counts = product_df['validation_reason'].value_counts(normalize=True).reset_index()
val_counts.columns = ['Validation Reason', 'Proportion']
val_counts = val_counts[val_counts['Proportion'] > 0.01]
if not val_counts.empty:
    val_counts['Count'] = (val_counts['Proportion'] * total_rows).round().astype(int)
    fig = px.bar(val_counts, x='Validation Reason', y='Count', color='Validation Reason', title='Validation Issues (>1%)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No validation issues exceed 1% threshold.")

# Category Distribution
st.subheader("📊 Category Distribution (Major Categories Only)")
cat_counts = product_df['category'].value_counts(normalize=True).reset_index()
cat_counts.columns = ['Category', 'Proportion']
cat_counts = cat_counts[cat_counts['Proportion'] > 0.01]
if not cat_counts.empty:
    cat_counts['Count'] = (cat_counts['Proportion'] * total_rows).round().astype(int)
    fig = px.pie(cat_counts, names='Category', values='Count', title='Product Category (>1%)', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No categories exceed 1% of total entries.")

# Missing Value Summary
st.subheader("🧼 Missing Value Summary")
missing_data = product_df.isnull().sum()
missing_df = pd.DataFrame({
    'Column': missing_data.index,
    'Missing Count': missing_data.values,
    'Percent Missing': (missing_data.values / total_rows * 100).round(2)
})
missing_df = missing_df[missing_df['Missing Count'] > 0]
if not missing_df.empty:
    st.table(missing_df)
else:
    st.success("No missing values found.")

# Valid vs Invalid Products Grouped by Category
st.subheader("✅ Valid vs Invalid Products by Category (>1% only)")
product_df['is_valid'] = product_df['validation_reason'].isnull()
status_group = product_df.groupby(['category', 'is_valid']).size().reset_index(name='count')
status_group = status_group[status_group['count'] / total_rows > 0.01]
status_group['Status'] = status_group['is_valid'].map({True: 'Valid', False: 'Invalid'})
if not status_group.empty:
    fig = px.bar(status_group, x='category', y='count', color='Status', barmode='group', title="Valid vs Invalid Products")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No valid/invalid groups exceed 1% of the data.")
