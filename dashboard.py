import matplotlib.pyplot as plt
import numpy as np

def plot_eps(bank_name):
    eps_data = {
        "State Bank of India": [10, 12, 15, 18, 17],
        "Kotak Mahindra Bank": [25, 27, 29, 30, 28],
        "Axis Bank": [20, 22, 21, 23, 24],
        "Bank of Baroda": [8, 10, 9, 12, 13],
        "HDFC Bank": [30, 32, 34, 36, 38],
        "ICICI Bank": [22, 24, 26, 27, 28]
    }
    
    years = np.arange(2020, 2025)
    
    if bank_name in eps_data:
        plt.figure(figsize=(8, 5))
        plt.plot(years, eps_data[bank_name], marker='o', linestyle='-', label=bank_name)
        plt.xlabel("Year")
        plt.ylabel("EPS")
        plt.title(f"Earnings Per Share (EPS) of {bank_name}")
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("Bank not found. Please enter a valid bank name.")

# Example usage
selected_bank = input("Enter the bank name: ")
plot_eps(selected_bank)
