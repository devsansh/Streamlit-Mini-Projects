import streamlit as st
import pandas as pd


DATA_FILE = 'file.csv'


def load_stock_data():
  try:
    df = pd.read_csv(DATA_FILE)
  except FileNotFoundError:
    st.error(f"Error: Could not find data file '{DATA_FILE}'. Please ensure it exists.")
    return None
  return df


df = load_stock_data()


if df is not None:  
  selected_stock = st.selectbox("Select Stock", df["symbol"])

  
  if selected_stock:
    selected_row = df[df["symbol"] == selected_stock]
    stock_name = selected_row["name"].iloc[0]
    st.write(f"You selected: {stock_name} ({selected_stock})")

