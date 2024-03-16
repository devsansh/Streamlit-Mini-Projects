import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Wall of Stocks:")
# Date settings:
st.header("Choose :blue[time_period]:red[:]")
today = datetime.now()
col1,col2 = st.columns(2)
with col1:
    st.subheader("Start Date:")
    start_date = st.date_input(label = "Enter start date",value= today - timedelta (days=10*365),format="YYYY-MM-DD")

with col2:
    st.subheader("End Date:")
    end_date = st.date_input(label = "Enter end date",value="default_value_today",format="YYYY-MM-DD")


all_stock_symbols = yf.Tickers('')

tickerSymbol = "GOOGL"
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='id', start=start_date, end=end_date)
st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
