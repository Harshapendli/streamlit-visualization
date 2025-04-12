import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="UrbanMart Dashboard", layout="wide")

st.title("📊 UrbanMart Business Insights Dashboard")

# FastAPI URL
API_URL = "http://localhost:8000"

# Fetch top customers
st.subheader("Top 5 Customers by Quantity Ordered")
resp = requests.get(f"{API_URL}/api/top_customers")
if resp.status_code == 200:
    top_customers = pd.Series(resp.json()).reset_index()
    top_customers.columns = ['Customer ID', 'Quantity']
    st.bar_chart(top_customers.set_index("Customer ID"))
else:
    st.error("Failed to fetch top customers.")

# Fetch top products
st.subheader("Top 5 Products by Quantity Ordered")
resp = requests.get(f"{API_URL}/api/top_products")
if resp.status_code == 200:
    top_products = pd.Series(resp.json()).reset_index()
    top_products.columns = ['Product ID', 'Quantity']
    st.line_chart(top_products.set_index("Product ID"))
else:
    st.error("Failed to fetch top products.")
