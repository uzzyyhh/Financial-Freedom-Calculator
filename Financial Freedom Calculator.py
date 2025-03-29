import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate years to financial freedom
def calculate_financial_freedom(income, expenses, savings_rate, investment_growth, target_amount):
    if expenses >= income:
        return float('inf'), []  # Return infinity years if savings are non-existent

    annual_savings = (income - expenses) * (savings_rate / 100)
    years = 0
    total_savings = 0
    savings_history = []

    while total_savings < target_amount:
        total_savings += annual_savings
        total_savings *= (1 + investment_growth / 100)
        years += 1
        savings_history.append(total_savings)

    return years, savings_history

# Streamlit UI
st.title("Financial Freedom Tracker")
st.sidebar.header("User Inputs")

# User Inputs
income = st.sidebar.number_input("Annual Income ($)", min_value=1000, value=50000, step=1000)
expenses = st.sidebar.number_input("Annual Expenses ($)", min_value=500, value=20000, step=500)
if expenses >= income:
    st.sidebar.error("Expenses should be less than income to generate savings.")
savings_rate = st.sidebar.slider("Savings Rate (%)", min_value=1, max_value=100, value=20)
investment_growth = st.sidebar.slider("Expected Investment Growth (%)", min_value=1, max_value=15, value=7)
target_amount = st.sidebar.number_input("Target Financial Freedom Amount ($)", min_value=10000, value=1000000, step=10000)

# Calculate Financial Freedom Timeline
years, savings_history = calculate_financial_freedom(income, expenses, savings_rate, investment_growth, target_amount)

# Display Results
st.subheader("Financial Freedom Calculation")
if years == float('inf'):
    st.write("🚨 **Unable to reach financial freedom with current inputs.** Consider increasing savings rate or reducing expenses.")
else:
    st.write(f"**Estimated Years to Financial Freedom:** {years} years")

    # Plot Wealth Growth
    fig, ax = plt.subplots()
    ax.plot(range(1, years+1), savings_history, marker='o', linestyle='-', color='b')
    ax.set_xlabel("Years")
    ax.set_ylabel("Total Savings ($)")
    ax.set_title("Projected Wealth Accumulation")
    ax.grid(True)
    st.pyplot(fig)

# Investment Portfolio Analysis
st.subheader("Investment Portfolio Analysis")
uploaded_file = st.file_uploader("Upload Your Investment CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if not df.empty:
        st.write("### Investment Data")
        st.dataframe(df)

        # Ensure necessary columns are present
        required_columns = {'Investment Name', 'Amount Invested', 'Current Value'}
        if required_columns.issubset(df.columns):
            # Calculate additional metrics
            df['Return ($)'] = df['Current Value'] - df['Amount Invested']
            df['Return (%)'] = (df['Return ($)'] / df['Amount Invested']) * 100

            # Display enhanced portfolio summary
            st.write("### Portfolio Summary")
            st.dataframe(df[['Investment Name', 'Amount Invested', 'Current Value', 'Return ($)', 'Return (%)']])

            # Portfolio-level metrics
            total_invested = df['Amount Invested'].sum()
            total_current_value = df['Current Value'].sum()
            total_return = total_current_value - total_invested
            total_return_percentage = (total_return / total_invested) * 100

            st.write(f"**Total Amount Invested:** ${total_invested:,.2f}")
            st.write(f"**Total Current Value:** ${total_current_value:,.2f}")
            st.write(f"**Total Portfolio Return:** ${total_return:,.2f} ({total_return_percentage:.2f}%)")

            # Visualize portfolio allocation
            fig, ax = plt.subplots()
            ax.pie(df['Current Value'], labels=df['Investment Name'], autopct='%1.1f%%', startangle=90)
            ax.set_title("Portfolio Allocation")
            st.pyplot(fig)
        else:
            st.warning(f"Uploaded file is missing required columns: {required_columns}")
    else:
        st.warning("Uploaded file is empty or invalid.")
