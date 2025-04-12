import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="UrbanMart Insights", layout="wide")
st.title("📊 UrbanMart Data Dashboard (Valid vs Invalid Data)")

uploaded_file = st.file_uploader("Upload JSON file with correct_data and incorrect_data", type=["json"])

if uploaded_file:
    json_data = json.load(uploaded_file)

    correct_df = pd.DataFrame(json_data.get("correct_data", []))
    incorrect_df = pd.DataFrame(json_data.get("incorrect_data", []))

    tab1, tab2, tab3 = st.tabs(["✅ Valid Data Insights", "❌ Invalid Data Summary", "📋 Raw Data"])

    with tab1:
        st.header("✅ Insights from Correct Data")

        if not correct_df.empty:
            st.subheader("1. Top 5 Customers by Spend")
            if "customer_id" in correct_df and "quantity" in correct_df and "price" in correct_df:
                correct_df["spend"] = correct_df["quantity"] * correct_df["price"]
                top_customers = correct_df.groupby("customer_id")["spend"].sum().nlargest(5).reset_index()
                fig = px.bar(top_customers, x="customer_id", y="spend", title="Top 5 Customers by Spend")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("2. Sales by Category")
            if "category" in correct_df and "price" in correct_df:
                category_sales = correct_df.groupby("category")["price"].sum().reset_index()
                fig = px.pie(category_sales, values="price", names="category", title="Sales by Category")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("3. Returns Over Time")
            if "date" in correct_df and "refund_amount" in correct_df:
                correct_df["date"] = pd.to_datetime(correct_df["date"], errors='coerce')
                returns_df = correct_df.dropna(subset=["date"]).groupby("date")["refund_amount"].sum().reset_index()
                fig = px.line(returns_df, x="date", y="refund_amount", title="Returns Over Time")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("4. Carrier Performance")
            if "carrier" in correct_df and "status" in correct_df:
                carrier_perf = correct_df.groupby(["carrier", "status"]).size().reset_index(name="count")
                fig = px.bar(carrier_perf, x="carrier", y="count", color="status", barmode="group",
                             title="Shipping Status by Carrier")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No valid records to display.")

    with tab2:
        st.header("❌ Data Quality Issues")

        if not incorrect_df.empty:
            col1, col2, col3 = st.columns(3)

            total_invalid = len(incorrect_df)
            missing_values = incorrect_df.isnull().sum().sum()
            negative_values = (incorrect_df.select_dtypes(include=['number']) < 0).sum().sum()

            col1.metric("❌ Invalid Records", total_invalid)
            col2.metric("🕳️ Missing Values", int(missing_values))
            col3.metric("📉 Negative Values", int(negative_values))

            st.markdown("---")

            st.subheader("🔍 Missing Fields Distribution")
            missing = incorrect_df.isnull().sum()
            missing = missing[missing > 0].sort_values(ascending=False)
            st.bar_chart(missing)
        else:
            st.info("No invalid records found!")

    with tab3:
        st.subheader("Correct Data")
        st.dataframe(correct_df, use_container_width=True)

        st.subheader("Incorrect Data")
        st.dataframe(incorrect_df, use_container_width=True)
