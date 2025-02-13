import streamlit as st
import yfinance as yf

def format_market_cap(value):
    if value >= 1e12:
        return f"{value / 1e12:.2f}T"
    elif value >= 1e9:
        return f"{value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"{value / 1e6:.2f}M"
    return str(value)

def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data[ticker] = {
            "Open": info.get("open", "N/A"),
            "Close": info.get("previousClose", "N/A"),
            "High": info.get("dayHigh", "N/A"),
            "Low": info.get("dayLow", "N/A"),
            "Market Cap": format_market_cap(info.get("marketCap", "N/A")),
            "Beta (5Y Monthly)": info.get("beta", "N/A"),
            "Volume": info.get("volume", "N/A"),
            "EPS (TTM)": info.get("trailingEps", "N/A"),
            "PE Ratio (TTM)": info.get("trailingPE", "N/A"),
            "Forward Dividend & Yield": info.get("dividendYield", "N/A"),
            "Avg. Volume": info.get("averageVolume", "N/A"),
            "Profit Margin": f"{info.get('profitMargins', 0) * 100:.2f}%" if info.get("profitMargins") else "N/A",
            "Return on Assets (TTM)": f"{info.get('returnOnAssets', 0) * 100:.2f}%" if info.get("returnOnAssets") else "N/A",
            "Return on Equity (TTM)": f"{info.get('returnOnEquity', 0) * 100:.2f}%" if info.get("returnOnEquity") else "N/A"
        }
    return data

tickers = {
    "HDFC Bank": "HDFCBANK.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Axis Bank": "AXISBANK.NS",
    "State Bank of India": "SBIN.NS",
    "ICICI Bank": "ICICIBANK.NS"
}

st.set_page_config(layout="wide")
st.title("Bank Stock Data Dashboard")

# Sidebar
st.sidebar.header("Stock Metrics")
selected_bank = st.sidebar.selectbox("Select a bank", list(tickers.keys()))

data = get_stock_data([tickers[selected_bank]])

ticker = tickers[selected_bank]
st.sidebar.subheader(selected_bank)
for key, value in data[ticker].items():
    st.sidebar.write(f"**{key}:** {value}")

# Sidebar for additional options
st.sidebar.header("Settings")
st.sidebar.write("Use the dropdown to select a bank and view key metrics.")

# Main content area
st.header(f"Stock Data for {selected_bank}")
if ticker in data:
    stock_data = data[ticker]
    st.write("### Key Stock Metrics")
    st.write(stock_data)
else:
    st.write("No data available.")
