# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 08:26:00 2023

@author: 27823
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title(":house-door: Home Loan Calculator ")

# Input fields for loan details
loan_amount = st.number_input("Loan Amount (R)", value=100000, step=1000)
interest_rate = st.number_input("Interest Rate (%)", value=4.5, step=0.1)
loan_term = st.number_input("Loan Term (Years)", value=30, step=1)

# Input fields for additional payments
extra_payment = st.number_input("Extra Monthly Payment (R)", value=0, step=100)

# Calculate monthly payment and create amortization table
monthly_interest_rate = interest_rate / 12 / 100
num_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * monthly_interest_rate
    * (1 + monthly_interest_rate) ** num_payments
) / ((1 + monthly_interest_rate) ** num_payments - 1)

if extra_payment > 0:
    total_payment = monthly_payment + extra_payment
else:
    total_payment = monthly_payment

st.subheader("Loan Details")
st.write(f"Monthly Payment: R{monthly_payment:.2f}")
st.write(f"Total Payment (including extra): R{total_payment:.2f}")

# Create an amortization table
amortization_df = pd.DataFrame(
    columns=["Month", "Payment", "Principal", "Interest", "Balance"]
)

balance = loan_amount
for month in range(1, num_payments + 1):
    interest_payment = balance * monthly_interest_rate
    principal_payment = total_payment - interest_payment
    balance -= principal_payment

    amortization_df = amortization_df.append(
        {
            "Month": month,
            "Payment": f"R{total_payment:.2f}",
            "Principal": f"R{principal_payment:.2f}",
            "Interest": f"R{interest_payment:.2f}",
            "Balance": f"R{balance:.2f}",
        },
        ignore_index=True,
    )

st.subheader("Amortization Table")
st.dataframe(amortization_df, hide_index=True)

# Allow users to change variables and see the impact
st.sidebar.subheader("Change Variables")
new_loan_amount = st.sidebar.number_input("New Loan Amount (R)", value=loan_amount, step=1000)
new_interest_rate = st.sidebar.number_input("New Interest Rate (%)", value=interest_rate, step=0.1)
new_loan_term = st.sidebar.number_input("New Loan Term (Years)", value=loan_term, step=1)
new_extra_payment = st.sidebar.number_input("New Extra Monthly Payment (R)", value=extra_payment, step=100)

# Calculate the impact of changes
new_monthly_interest_rate = new_interest_rate / 12 / 100
new_num_payments = new_loan_term * 12
new_monthly_payment = (
    new_loan_amount
    * new_monthly_interest_rate
    * (1 + new_monthly_interest_rate) ** new_num_payments
) / ((1 + new_monthly_interest_rate) ** new_num_payments - 1)

if new_extra_payment > 0:
    new_total_payment = new_monthly_payment + new_extra_payment
else:
    new_total_payment = new_monthly_payment

st.sidebar.subheader("Impact of Changes")
st.sidebar.write(f"New Monthly Payment: R{new_monthly_payment:.2f}")
st.sidebar.write(f"New Total Payment (including extra): R{new_total_payment:.2f}")

# Calculate and display the savings or additional cost
payment_difference = new_total_payment - total_payment
st.sidebar.write(f"Difference: R{payment_difference:.2f} {'savings' if payment_difference < 0 else 'additional cost'}")

