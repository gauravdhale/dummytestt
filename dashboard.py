import yfinance as yf
import matplotlib.pyplot as plt

# List of companies
companies = ['HDFC Bank', 'ICICI Bank', 'State Bank of India', 'Kotak Mahindra Bank', 'Axis Bank', 'Bank of Baroda']

# Fetch EPS data
eps_data = {}
for company in companies:
    stock = yf.Ticker(company)
    eps = stock.info['forwardPE']
    eps_data[company] = eps

# Plot EPS data
plt.figure(figsize=(10, 6))
plt.bar(eps_data.keys(), eps_data.values())
plt.xlabel('Company')
plt.ylabel('EPS')
plt.title('EPS of Various Companies')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
