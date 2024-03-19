import streamlit as st
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from datetime import datetime, timedelta
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

st.title("WALL OF STOCKS📈:")


#----------------------------#

#Def to load Stock names in SelectBox
DATA_FILE = 'file.csv'

def load_stock_data():
  try:
    df = pd.read_csv(DATA_FILE)
  except FileNotFoundError:
    st.error(f"Error: Could not find data in storage.'{DATA_FILE}'. Please ensure it exists.")
    return None
  return df

df = load_stock_data()

if df is not None:  
  ticker = st.selectbox("Select Stock", df["symbol"])

  if ticker:
    selected_row = df[df["symbol"] == ticker]
    stock_name = selected_row["name"].iloc[0]
    st.write(f"You selected: {stock_name} ({ticker})")

#----------------------------# 
#Create multple tabs 
#----------------------------# 
main_container = st.container(border=True,height=93)
column_1,column_2,column_3 = main_container.columns(3,gap="medium")

with column_1:
  container_1=st.container(height=60)
  container_1.write("Test-Case")
  
with column_2:
  container_2=st.container(height=60)
  container_2.write("Test-Case")
with column_3:
  container_3 = st.container(height=60)
  container_3.write("Test-Case")
  
#----------------------------#