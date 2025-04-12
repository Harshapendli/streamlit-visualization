import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Business Insights & Product Quality", layout="wide")

# Sidebar navigation
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
            st.subheader("🛍️ Top 5 Products by Revenue")
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
            st.plotly_chart(px.pie(top_refunds, names='reason', values='total_refund_amount'), use_container_width=True)

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
        val_counts.columns = ['Validation Reason', 'Proportion']
        val_counts = val_counts[val_counts['Proportion'] > 0.01]

        if not val_counts.empty:
            val_counts['Count'] = (val_counts['Proportion'] * total_rows).round().astype(int)
            fig1 = px.bar(val_counts, x='Validation Reason', y='Count', color='Validation Reason',
                          title='Validation Issues (>1% of records)', height=400)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No validation issues exceed 1% threshold.")

        st.subheader("📊 Category Distribution (Major Categories Only)")
        cat_counts = df['category'].value_counts(normalize=True).reset_index()
        cat_counts.columns = ['Category', 'Proportion']
        cat_counts = cat_counts[cat_counts['Proportion'] > 0.01]

        if not cat_counts.empty:
            cat_counts['Count'] = (cat_counts['Proportion'] * total_rows).round().astype(int)
            fig2 = px.pie(cat_counts, names='Category', values='Count', title='Product Category', hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No categories exceed 1% of total entries.")

        st.subheader("🧼 Missing Value Summary")
        missing_data = df.isnull().sum()
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

        st.subheader("🧾 Invalid Products by Category (Word Map)")

# Filter only invalid records
invalid_df = df[df['validation_reason'].notnull()]

# Create category frequency dictionary
invalid_counts = invalid_df['category'].value_counts()
category_freq = invalid_counts.to_dict()

if category_freq:
    # Generate word cloud
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(category_freq)

    # Show the word cloud using matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
else:
    st.info("No invalid products to display in word map.")

        # ✅ Raw Data Preview moved to the end
        st.subheader("🧾 Raw Data Preview")
        st.dataframe(df)

    except Exception as e:
        st.error(f"🚨 Failed to load data from GitHub: {e}")
        st.markdown(
            """
            - Please make sure the file exists and is accessible at the raw GitHub URL.  
            - Make sure the CSV is properly formatted (equal columns, quoted text).  
            - You can test by copying this link and opening it in your browser.  
            """
        )

# ---------------- Page Routing ----------------
if page == "📈 Business Insights":
    show_business_insights()
else:
    show_data_quality_dashboard()
