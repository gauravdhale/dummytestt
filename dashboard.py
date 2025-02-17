import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

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
    financials = stock.financials.T  # Transpose to get years as rows
    eps_data[company] = financials['Earnings']

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
