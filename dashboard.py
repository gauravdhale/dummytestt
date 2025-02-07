import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# List of banking sector stocks
banking_stocks = {
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bank of Baroda": "BANKBARODA.NS"
}

def fetch_stock_data(ticker, period="5y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def plot_heatmap(correlation_matrix):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

st.set_page_config(page_title="Banking Sector Dashboard", layout="wide")
st.title("Banking Sector Financial Dashboard")

# Fetching all stock data for correlation heatmap
all_stock_data = {name: fetch_stock_data(ticker) for name, ticker in banking_stocks.items()}
closing_prices = pd.DataFrame({name: data["Close"] for name, data in all_stock_data.items() if not data.empty})

if not closing_prices.empty:
    correlation_matrix = closing_prices.corr()
    st.subheader("Correlation Heatmap of Banking Stocks")
    plot_heatmap(correlation_matrix)
else:
    st.warning("Not enough data for correlation analysis.")
