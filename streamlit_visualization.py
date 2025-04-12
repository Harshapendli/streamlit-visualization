import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Product Data Quality Dashboard", layout="wide")

st.title("📦 Product Data Quality Dashboard")

uploaded_file = st.file_uploader("Upload `products.csv` with validation issues", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🧾 Raw Data Preview")
    st.dataframe(df)

    # Strip whitespace from category
    df['category'] = df['category'].astype(str).str.strip()

    total_rows = len(df)

    # ---- 1. Validation Issue Count (filtered to >1%) ----
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

    # ---- 2. Category Distribution Pie Chart (filtered to >1%) ----
    st.subheader("📊 Category Distribution (Major Categories Only)")
    cat_counts = df['category'].value_counts(normalize=True).reset_index()
    cat_counts.columns = ['Category', 'Proportion']
    cat_counts = cat_counts[cat_counts['Proportion'] > 0.01]

    if not cat_counts.empty:
        cat_counts['Count'] = (cat_counts['Proportion'] * total_rows).round().astype(int)
        fig2 = px.pie(cat_counts, names='Category', values='Count', title='Product Category (>1%)', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No categories exceed 1% of total entries.")

    # ---- 3. Missing Value Summary ----
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

    # ---- 4. Valid vs Invalid Products Grouped by Category ----
    st.subheader("✅ Valid vs Invalid Products by Category (>1% only)")
    df['is_valid'] = df['validation_reason'].isnull()
    status_group = df.groupby(['category', 'is_valid']).size().reset_index(name='count')

    # Add only rows where (count / total) > 1%
    status_group = status_group[status_group['count'] / total_rows > 0.01]
    status_group['Status'] = status_group['is_valid'].map({True: 'Valid', False: 'Invalid'})

    if not status_group.empty:
        fig4 = px.bar(status_group, x='category', y='count', color='Status', barmode='group',
                      title="Valid vs Invalid Products by Category (>1%)")
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No valid/invalid groups exceed 1% of the data.")
