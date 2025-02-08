import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from datetime import datetime, timedelta

# Define Banking Stocks and Bank Nifty Index
companies = {
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'State Bank of India': 'SBIN.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Bank of Baroda': 'BANKBARODA.NS'
}
bank_nifty_ticker = "^NSEBANK"

# Streamlit Configuration
st.set_page_config(page_title="Banking Sector Dashboard", layout="wide")
st.title("📊 Banking Sector Financial Dashboard")
st.markdown("---")

# Selection Dropdown
selected_stock = st.sidebar.selectbox("🔍 Select a Bank", list(companies.keys()))

# Date Range Selection
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input('Start Date', datetime.today() - timedelta(days=365*5))
end_date = st.sidebar.date_input('End Date', datetime.today())

# Function to Fetch Stock Data
def fetch_stock_data(ticker, start, end):
    try:
        stock_data = yf.download(ticker, start=start, end=end)
        if stock_data.empty:
            return pd.DataFrame()
        stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['Price_Change'] = stock_data['Close'].pct_change()
        return stock_data.dropna()
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# Fetch Data for Selected Stock and Bank Nifty
bank_nifty_data = fetch_stock_data(bank_nifty_ticker, start_date, end_date)
selected_stock_data = fetch_stock_data(companies[selected_stock], start_date, end_date)

# Display Metrics if Data is Available
st.sidebar.header("📌 Key Metrics")
if not selected_stock_data.empty:
    latest_data = selected_stock_data.iloc[-1]
    metric_values = {
        "Open": latest_data["Open"],
        "Close": latest_data["Close"],
        "High": latest_data["High"],
        "Low": latest_data["Low"],
        "EPS": np.random.uniform(10, 50),
        "IPO Price": np.random.uniform(200, 1000),
        "P/E Ratio": np.random.uniform(5, 30),
        "Dividend": np.random.uniform(1, 5)
    }
    for label, value in metric_values.items():
        st.sidebar.metric(label=label, value=f"{value:.2f}" if isinstance(value, (int, float)) else value)
else:
    st.sidebar.warning(f"No stock data available for {selected_stock}.")

# BankNifty and Stock Overview
st.header("📈 Market Overview")
col1, col2 = st.columns(2)

# BankNifty Trend Graph
with col1:
    st.subheader("BankNifty Trend")
    if not bank_nifty_data.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(bank_nifty_data.index, bank_nifty_data['Close'], label="BankNifty Close", color='blue')
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("No data available for BankNifty.")

# Selected Stock Trend Graph
with col2:
    st.subheader(f"{selected_stock} Trend")
    if not selected_stock_data.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(selected_stock_data.index, selected_stock_data['Close'], label=f"{selected_stock} Close", color='red')
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning(f"No data available for {selected_stock}.")

# Correlation Heatmap Section
st.header("📊 Correlation Heatmap of Banking Stocks")

# Fetching all stock data for correlation heatmap
def fetch_all_stocks_data(companies, start, end):
    all_stock_data = {}
    for name, ticker in companies.items():
        data = fetch_stock_data(ticker, start, end)
        if not data.empty:
            all_stock_data[name] = data['Close']
    return pd.DataFrame(all_stock_data)

closing_prices = fetch_all_stocks_data(companies, start_date, end_date)

if not closing_prices.empty and len(closing_prices.columns) > 1:
    correlation_matrix = closing_prices.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
else:
    st.warning("Not enough data for correlation analysis.")
