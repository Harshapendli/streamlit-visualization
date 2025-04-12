import streamlit as st
import pandas as pd
import plotly.express as px

# Upload CSV
st.title("📦 Product Data Quality Dashboard")

uploaded_file = st.file_uploader("Upload `products.csv` with validation issues", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🧾 Raw Data Preview")
    st.dataframe(df)

    # Clean whitespace in category
    df['category'] = df['category'].str.strip()

    # 📌 1. Validation Issues Count
    st.subheader("❗ Count of Validation Issues")
    validation_counts = df['validation_reason'].value_counts().reset_index()
    validation_counts.columns = ['Validation Reason', 'Count']
    fig1 = px.bar(validation_counts, x='Validation Reason', y='Count', color='Validation Reason',
                  title='Validation Issue Counts', height=400)
    st.plotly_chart(fig1, use_container_width=True)

    # 📌 2. Pie Chart for Category Distribution (Valid or Not)
    st.subheader("📊 Category Distribution (Raw)")
    fig2 = px.pie(df, names='category', title='Product Category Distribution', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    # 📌 3. Summary of Missing Values
    st.subheader("🧼 Missing Value Summary")
    missing_data = df.isnull().sum().reset_index()
    missing_data.columns = ['Column', 'Missing Count']
    st.table(missing_data[missing_data['Missing Count'] > 0])

    # 📌 4. Valid vs Invalid Products Grouped by Category
    st.subheader("✅ Valid vs Invalid Products by Category")
    df['is_valid'] = df['validation_reason'].isnull()
    validity_group = df.groupby(['category', 'is_valid']).size().reset_index(name='count')
    validity_group['Status'] = validity_group['is_valid'].map({True: 'Valid', False: 'Invalid'})

    fig4 = px.bar(validity_group, x='category', y='count', color='Status', barmode='group',
                  title="Validity Status by Category")
    st.plotly_chart(fig4, use_container_width=True)
