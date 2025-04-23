import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Business Insights & Product Quality", layout="wide")

# Sidebar navigation page
page = st.sidebar.radio("Go to", ["📈 Business Insights", "📦 Product Data Quality"])

# ---------------- Business Insights ----------------
def show_business_insights():
    st.title("📈 Business Insights Report")

    METRICS_URL = "https://raw.githubusercontent.com/Harshapendli/streamlit-visualization/main/business_metrics.csv"

    @st.cache_data
    def load_metrics(url):
        return pd.read_csv(url)

    try:
        df = load_metrics(METRICS_URL)

        if {'customer_id', 'customer_name', 'total_spent'}.issubset(df.columns):
            st.subheader("🏅 Top 5 Customers by Total Spend")
            top_customers = df.groupby(['customer_id', 'customer_name'])['total_spent'].sum().nlargest(5).reset_index()
            st.dataframe(top_customers)
            st.plotly_chart(px.bar(top_customers, x='customer_name', y='total_spent', color='customer_name'), use_container_width=True)

        if {'product_id', 'product_name', 'total_revenue'}.issubset(df.columns):
            st.subheader("🛍 Top 5 Products by Revenue")
            top_products = df.groupby(['product_id', 'product_name'])['total_revenue'].sum().nlargest(5).reset_index()
            st.dataframe(top_products)
            st.plotly_chart(px.bar(top_products, x='product_name', y='total_revenue', color='product_name'), use_container_width=True)

        if {'carrier', 'on_time_deliveries'}.issubset(df.columns):
            st.subheader("🚚 Top 5 Shipping Carriers by On-Time Deliveries")
            top_carriers = df.groupby('carrier')['on_time_deliveries'].sum().nlargest(5).reset_index()
            st.dataframe(top_carriers)
            st.plotly_chart(px.bar(top_carriers, x='carrier', y='on_time_deliveries', color='carrier'), use_container_width=True)

        if {'reason', 'total_refund_amount'}.issubset(df.columns):
            st.subheader("💸 Top 5 Return Reason Analysis")
            top_refunds = df.groupby('reason')['total_refund_amount'].sum().nlargest(5).reset_index()
            st.dataframe(top_refunds)
            # Convert pie chart to donut chart
            fig = px.pie(top_refunds, names='reason', values='total_refund_amount', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Failed to load business metrics: {e}")

# ---------------- Product Data Quality ----------------
def show_data_quality_dashboard():
    st.title("📦 Product Data Quality Dashboard")

    GITHUB_CSV_URL = "https://raw.githubusercontent.com/Harshapendli/streamlit-visualization/main/incorrect_products.csv"

    @st.cache_data
    def load_data(url):
        try:
            return pd.read_csv(url, engine='python', on_bad_lines='warn')
        except Exception as e:
            st.stop()
            st.error(f"Error reading CSV: {e}")

    try:
        df = load_data(GITHUB_CSV_URL)
        df['category'] = df['category'].astype(str).str.strip()
        total_rows = len(df)

        st.subheader("❗ Frequent Validation Issues")
        val_counts = df['validation_reason'].value_counts(normalize=True).reset_index()
        val_counts_
