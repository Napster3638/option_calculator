# Nifty Option Entry & Averaging Calculator App

import streamlit as st
import pandas as pd

st.title("Option Entry & Averaging Calculator")

# ----- Inputs -----
st.header("Input Parameters")

option_price = st.number_input("Option Price", value=120.0, step=1.0)
reduction_percent = st.number_input("Reduction Factor (%)", value=10.0, step=1.0)
lot_size = st.number_input("Lot Size", value=75, step=1)
initial_lots = st.number_input("Initial Lots", value=4, step=1)
max_additional_lots = st.number_input("Max Additional Lots at Last Step", value=2, step=1)
stoploss_percent = st.number_input("Stop-Loss Percentage (%)", value=35.0, step=1.0)  # 🔹 new input

# ----- Calculation -----
prices = [option_price]
lots_sequence = [initial_lots, 1, 1, 1, max_additional_lots]  # fixed sequence
for i in range(1, len(lots_sequence)):
    prices.append(prices[-1] * (1 - reduction_percent/100))

# Build table
data = []
cumulative_lots = 0
cumulative_cost = 0
for i, (p, l) in enumerate(zip(prices, lots_sequence)):
    cumulative_lots += l
    cost_step = p * l * lot_size
    cumulative_cost += cost_step
    # MTM Loss at entry price for previous lots
    mtm_loss = sum([(prev_p - p) * lot_size * prev_l for prev_p, prev_l in zip(prices[:i], lots_sequence[:i])])
    data.append([i+1, round(p,2), l, cumulative_lots, round(cost_step,2), round(cumulative_cost,2), round(mtm_loss,2)])

df = pd.DataFrame(data, columns=[
    "Step", "Entry Price", "Lots Bought", "Cumulative Lots", 
    "Cost This Step", "Cumulative Capital", "MTM Loss at Entry Price"
])

# ----- Mini Table -----
# st.subheader("Entry Snapshot")
# mini_df = df[["Entry Price", "Lots Bought", "MTM Loss at Entry Price"]]
# st.dataframe(mini_df)
st.subheader("Entry Snapshot")

# 🔹 Add CSS to increase font size in tables
st.markdown("""
    <style>
    .dataframe td, .dataframe th {
        font-size: 220px !important;  /* change number to adjust */
    }
    </style>
    """, unsafe_allow_html=True)

mini_df = df[["Entry Price", "Lots Bought", "MTM Loss at Entry Price"]]
st.dataframe(mini_df)  # interactive table with larger font

# ----- Summary Outputs -----
total_capital = df["Cumulative Capital"].iloc[-1]
average_price = sum([p*l for p,l in zip(prices, lots_sequence)]) / sum(lots_sequence)
stoploss_amount = total_capital * (stoploss_percent / 100)  # 🔹 now uses user input
stoploss_price = (total_capital - stoploss_amount) / (sum(lots_sequence) * lot_size)

st.subheader("Summary Outputs")
st.metric("Total Capital Employed", round(total_capital,2))
st.metric("Average Buy Price", round(average_price,2))
st.metric(f"Stop-Loss Amount ({stoploss_percent:.0f}% Capital)", round(stoploss_amount,2))
st.metric("Stop-Loss Trigger Price", round(stoploss_price,2))

# ----- Full Table (bottom) -----
st.subheader("Detailed Stepwise Entry & MTM Loss Table")
st.dataframe(df)




