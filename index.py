import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

def get_data():
    conn = mysql.connector.connect(
        host="localhost", user="root", password="leap54", database="e_commerce"
    )
    query = """
        SELECT InvoiceDate, Quantity, UnitPrice, Country, StockCode, CustomerID
        FROM E_comm
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = get_data()
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

st.title("📊 E-Commerce Sales Dashboard")
st.sidebar.header("Filters")

date_range = st.sidebar.date_input("Select Date Range", [df.InvoiceDate.min(), df.InvoiceDate.max()])
df_filtered = df[(df.InvoiceDate.dt.date >= date_range[0]) & (df.InvoiceDate.dt.date <= date_range[1])]

st.subheader("💰 Monthly Revenue")
df_filtered['Month'] = df_filtered['InvoiceDate'].dt.to_period('M')
monthly_revenue = df_filtered.groupby('Month')['TotalPrice'].sum()
fig, ax = plt.subplots()
monthly_revenue.plot(kind='bar', ax=ax, color='blue')
ax.set_ylabel("Revenue")
st.pyplot(fig)

st.subheader("🔥 Top 10 Best-Selling Products")
top_products = df_filtered.groupby('StockCode')['Quantity'].sum().nlargest(10)
fig, ax = plt.subplots()
top_products.plot(kind='bar', ax=ax, color='orange')
ax.set_ylabel("Total Quantity Sold")
st.pyplot(fig)

st.subheader("🌍 Sales Distribution by Country")
country_sales = df_filtered.groupby('Country')['TotalPrice'].sum().nlargest(10)
fig, ax = plt.subplots()
country_sales.plot(kind='bar', ax=ax, color='green')
ax.set_ylabel("Revenue")
st.pyplot(fig)

st.write("📌 Data Source: MySQL Database")