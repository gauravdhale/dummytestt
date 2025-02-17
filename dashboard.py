import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_eps(bank_name):
    eps_data = {
        "State Bank of India": [22.15, 25.11, 39.64, 62.23, 75.17, 88.91],
        "Kotak Mahindra Bank": [18.49, 20.25, 38.62, 52.77, 61.41, 113.32],
        "Axis Bank": [-60.94, -33.64, 18.46, 21.76, 67.38, 91.02],
        "Bank of Baroda": [-45.33, -27.55, -11.08, 13.48, 22.65, 39.50],
        "HDFC Bank": [25.74, 27.96, 39.49, 57.69, 53.82, 90.95],
        "ICICI Bank": [-9.46, -0.03, 21.15, 36.13, 53.04, 69.66]
    }
    
    years = np.array([2020, 2021, 2022, 2023, 2024,2025])
    
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
plot_eps(bank_name)
