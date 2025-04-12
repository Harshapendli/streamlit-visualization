from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow frontend (Streamlit) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load your cleaned data (replace with your path or logic)
df_orders = pd.read_csv("incorrect_products.csv")
df_customers = pd.read_csv("incorrect_products.csv")

@app.get("/api/top_customers")
def get_top_customers():
    top = df_orders.groupby("customer_id")["quantity"].sum().sort_values(ascending=False).head(5)
    return top.to_dict()

@app.get("/api/top_products")
def get_top_products():
    top = df_orders.groupby("product_id")["quantity"].sum().sort_values(ascending=False).head(5)
    return top.to_dict()
