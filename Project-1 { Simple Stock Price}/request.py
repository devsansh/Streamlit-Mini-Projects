import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
API_KEY = 'C6MLI6ZMEUDMGA3L'

def fetch_stock_data(symbol, start_date, end_date):
  url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&datatype=csv&startDate={start_date}&endDate={end_date}"
  response = requests.get(url)
  if response.status_code == 200:
    return pd.read_csv(response.content)
  else:
    st.error(f"Error fetching data for {symbol}. Status code: {response.status_code}")
    return None

st.title("Wall of Stocks:")

# Date settings:
st.header("Choose Time Period:")
today = datetime.now()
col1, col2 = st.columns(2)
with col1:
  st.subheader("Start Date:")
  start_date = st.date_input(label="Enter start date", value=today - timedelta(days=10 * 365), format="YYYY-MM-DD")

with col2:
  st.subheader("End Date:")
  today = datetime.now()  # Get the current date and time
  end_date = st.date_input(label="Enter end date", value=today) 
# User input for stock symbol

###############
  
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
  selected_stock = st.selectbox("Select Stock", df["symbol"])

  if selected_stock:
    selected_row = df[df["symbol"] == selected_stock]
    stock_name = selected_row["name"].iloc[0]
    st.write(f"You selected: {stock_name} ({selected_stock})")


###############
tickerSymbol =st.button("Show Visuals","Primary")
# Fetch data if symbol and dates are provided
if tickerSymbol and start_date and end_date:
  tickerDf = fetch_stock_data(tickerSymbol, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
  if tickerDf is not None:
    # Assuming 'timestamp' is the date column and '4. close' is the closing price
    st.line_chart(tickerDf[["timestamp", "4. close"]], x="timestamp", y="4. close", label="Closing Price")
    # Assuming '5. volume' is the volume column
    st.line_chart(tickerDf[["timestamp", "5. volume"]], x="timestamp", y="5. volume", label="Volume")

