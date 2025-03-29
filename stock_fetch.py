import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

# Your Alpha Vantage API Key
API_KEY = "R9A0KWPR91D28XCB"

# List of US stock symbols
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.B", "JPM", "V"]

# Initialize Alpha Vantage API
ts = TimeSeries(key=API_KEY, output_format="pandas")

# Dictionary to store stock data
stock_data = {}

# Fetch data for each stock
for symbol in stocks:
    try:
        data, meta_data = ts.get_daily(symbol=symbol, outputsize="full")
        data.columns = ["Open", "High", "Low", "Close", "Volume"]
        data.index = pd.to_datetime(data.index)
        stock_data[symbol] = data
        print(f"✅ Fetched data for {symbol}")
        
        # Save to CSV
        data.to_csv(f"{symbol}_historical_data.csv")
        
        # To avoid API rate limits (5 requests per minute for free tier)
        time.sleep(12)  

    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")

# Print sample data
print("\n📊 Sample Data for AAPL:")
print(stock_data["AAPL"].head())
