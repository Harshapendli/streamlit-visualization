import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data Dashboard")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Data cleaning steps
    df = df.drop_duplicates()
    df = df.dropna()
    
    # Display data
    st.write(df.head())
    
    # Visualization
    if 'column_name' in df.columns:
        st.subheader("Line Chart")
        st.line_chart(df['column_name'])
    else:
        st.warning("Column 'column_name' not found in the data.")

    if 'numeric_column' in df.columns:
        st.subheader("Histogram")
        fig, ax = plt.subplots()
        ax.hist(df['numeric_column'])
        st.pyplot(fig)
    else:
        st.warning("Column 'numeric_column' not found in the data.")
