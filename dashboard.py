import streamlit as st
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
    
    years = np.array([2020, 2021, 2022, 2023, 2024])
    
    if bank_name in eps_data:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(years, eps_data[bank_name], marker='o', linestyle='-', label=bank_name)
        ax.set_xlabel("Year")
        ax.set_ylabel("EPS")
        ax.set_title(f"Earnings Per Share (EPS) of {bank_name}")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.error(f"Bank '{bank_name}' not found. Please select a valid bank.")

st.title("Bank EPS Visualization")
bank_name = st.selectbox("Select a bank:", ["State Bank of India", "Kotak Mahindra Bank", "Axis Bank", "Bank of Baroda", "HDFC Bank", "ICICI Bank"])
if st.button("Show EPS Graph"):
    plot_eps(bank_name)
