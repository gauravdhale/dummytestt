import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import seaborn as sns

# Define Banking Stocks and Bank Nifty Index
companies = {
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'State Bank of India': 'SBIN.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Bank of Baroda': 'BANKBARODA.NS'
}

csv_files = {
    'HDFC Bank': 'HDFCBANK.csv',
    'ICICI Bank': 'ICICI_BANK.csv',
    'State Bank of India': 'SBI.csv',
    'Kotak Mahindra Bank': 'KOTAK.csv',
    'Axis Bank': 'AXIS.csv',
    'Bank of Baroda': 'BARODA.csv'
}
bank_nifty_ticker = "^NSEBANK"

# Streamlit Configuration
st.set_page_config(page_title="Banking Sector Dashboard", layout="wide")
st.title("\ud83d\udcca Banking Sector Financial Dashboard")
st.markdown("---")

# Selection Dropdown
selected_stock = st.sidebar.selectbox("\ud83d\udd0d Select a Bank", list(companies.keys()))

# Function to Fetch Stock Data
def fetch_stock_data(ticker, period="5y"):
    try:
        stock_data = yf.download(ticker, period=period, interval="1d")
        if stock_data.empty:
            return pd.DataFrame()
        stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['Price_Change'] = stock_data['Close'].pct_change()
        return stock_data.dropna()
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# Fetch Data
bank_nifty_data = fetch_stock_data(bank_nifty_ticker)
selected_stock_data = fetch_stock_data(companies[selected_stock])

# Heatmap Section
st.header("Nifty Bank Composition Heatmap")
github_url = st.text_input("Enter the GitHub CSV file URL", value="https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/heatmap.csv")

if github_url:
    try:
        df = pd.read_csv(github_url, encoding='ISO-8859-1')
        if 'Company' in df.columns:
            df.set_index('Company', inplace=True)
        else:
            st.write("Error: 'Company' column not found in the CSV file.")
        
        if 'Weight(%)' in df.columns:
            plt.figure(figsize=(6,8))
            heatmap_data = df[['Weight(%)']]
            sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', cbar=True)
            plt.title('Nifty Bank Composition Heatmap')
            plt.ylabel('Company')
            plt.xlabel('')
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.write("HEAT MAP ")
    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please upload a CSV file or enter a valid GitHub URL.")
