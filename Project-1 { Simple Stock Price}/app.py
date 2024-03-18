import streamlit as st
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from datetime import datetime, timedelta
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData

#------------------------------------#

st.title("Walls of Stocks:")

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
    st.write(f"You selected: {stock_name} ({ticker})")###

#-----------------------------------------------------#
with st.sidebar:   
    st.header("Choose :blue[time_period]:red[:]")
    today = datetime.now()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Start Date:")
        start_date = st.date_input(label="Enter start date", value=today - timedelta(days=5 * 365), format="YYYY-MM-DD")

    with col2:
        st.subheader("End Date:")
        today = datetime.now()  # Get the current date and time
        end_date = st.date_input(label="Enter end date", value=today) 


ticker_data = yf.download(ticker,start = start_date, end = end_date )

#st.write(ticker_data)

figure_1 = px.line(ticker_data, x = ticker_data['Adj Close'],title = ticker)
st.plotly_chart(figure_1)

pricing_data, fundamental_data, news = st.tabs(["Pricing Board:","Fundamental Charts:","Latest News:"])
with pricing_data:
   st.subheader('Price Movements')
   price_change_data = ticker_data
   price_change_data['% Change']= ticker_data['Adj Close'] / ticker_data['Adj Close'].shift(1) - 1
   price_change_data.dropna(inplace = True)
   st.write(price_change_data)
   annul_returns = price_change_data['% Change'].mean()*252*100
   st.write('Annual return:',annul_returns,"%")
   std_deviation = np.std(price_change_data['% Change'])*np.sqrt(252)
   st.write('Standard Deviation:',std_deviation*100,'%')
   st.write('Risk Adj. return:',std_deviation*100,"%")

#-------------------------------------------------------#
with fundamental_data:
   st.subheader('Fundamental')
   API_KEY = 'C6MLI6ZMEUDMGA3L'
   fundamental = FundamentalData(API_KEY,output_format = 'pandas')
   st.subheader('Balance Sheet:')
   balance_sheet = fundamental.get_balance_sheet_annual(ticker)[0]
   balance_sheet_1 =balance_sheet.T[2:]
   balance_sheet_1.columns = list(balance_sheet.T.iloc[0])
   st.write(balance_sheet_1)

   # ********************** #
   
   st.subheader("Income Statement:")
   income_statement = fundamental.get_income_statement_annual(ticker)[0]
   income_statement_1 = income_statement.T[2:]
   income_statement_1.columns = list(income_statement.T.iloc[0])
   st.write(income_statement_1)

   #**********************#

   st.subheader('Cash Flow Statement:')
   cash_flow = fundamental.get_cash_flow_annual(ticker)[0]
   cash_flow_1 = cash_flow.T[2:]
   cash_flow_1.columns = list(cash_flow.T.iloc[0])
   st.write(cash_flow_1)   
#-------------------------------------------------------#
with news:
   st.subheader('Latest TOP10')
   