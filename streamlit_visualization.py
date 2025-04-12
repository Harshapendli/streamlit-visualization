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
    st.subheader("Line Chart")
    st.line_chart(df['column_name'])
    
    st.subheader("Histogram")
    fig, ax = plt.subplots()
    ax.hist(df['numeric_column'])
    st.pyplot(fig)
