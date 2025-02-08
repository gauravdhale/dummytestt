import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

# Fix UnicodeEncodeError
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Title
st.title("\U0001F4CA Banking Sector Financial Dashboard")

# Banking Stocks List
BANKING_STOCKS = {
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bank of Baroda": "BANKBARODA.NS"
}

# Sidebar Selection
selected_stock = st.sidebar.selectbox("Select a Bank Stock", list(BANKING_STOCKS.keys()))
ticker = BANKING_STOCKS[selected_stock]

# Fetch Historical Data
def get_stock_data(ticker, period="5y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

data = get_stock_data(ticker)

# Stock Price Line Chart
st.subheader(f"{selected_stock} Stock Price (Last 5 Years)")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Closing Price'))
fig.update_layout(title=f"{selected_stock} Stock Price Trend", xaxis_title='Date', yaxis_title='Price (INR)')
st.plotly_chart(fig)

# Predict Future Prices using LSTM
st.subheader("📈 Stock Price Prediction using LSTM")

# Data Preprocessing
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data['Close'].values.reshape(-1,1))

train_size = int(len(data_scaled) * 0.8)
train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]

def create_dataset(data, time_step=50):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

X_train, y_train = create_dataset(train_data)
X_test, y_test = create_dataset(test_data)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build LSTM Model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    LSTM(50, return_sequences=False),
    Dense(25),
    Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=5, batch_size=16, verbose=0)

# Predict Stock Prices
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions.reshape(-1, 1))

dates = data.index[train_size + 51:]
st.line_chart(pd.DataFrame({'Actual': data['Close'][train_size + 51:], 'Predicted': predictions[:, 0]}, index=dates))

# Sectoral KPIs
st.subheader("📊 Sector Financial Metrics")
kpi_data = {
    "Metric": ["Earnings Per Share (EPS)", "P/E Ratio", "IPO Price"],
    "HDFC Bank": [80, 22, 2250],
    "ICICI Bank": [60, 20, 1000],
    "SBI": [45, 18, 250],
    "Kotak Mahindra Bank": [70, 25, 1400],
    "Axis Bank": [55, 19, 400],
    "Bank of Baroda": [30, 12, 120]
}

kpi_df = pd.DataFrame(kpi_data)
st.table(kpi_df)
