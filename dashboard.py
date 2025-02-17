import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# List of companies and their corresponding Yahoo Finance tickers
companies = {
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'State Bank of India': 'SBIN.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Bank of Baroda': 'BANKBARODA.NS'
}

# Fetch EPS data
eps_data = pd.DataFrame()

for company, ticker in companies.items():
    stock = yf.Ticker(ticker)
    earnings = stock.earnings
    if not earnings.empty:
        eps_data[company] = earnings['Earnings Per Share']

# Transpose the DataFrame to have years as rows
eps_data = eps_data.T

# Plot EPS data
eps_data.plot(kind='bar', figsize=(12, 6))
plt.title('EPS of Various Companies')
plt.xlabel('Year')
plt.ylabel('EPS')
plt.legend(title='Company')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
