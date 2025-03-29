import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Define paths
CLEANED_FOLDER = r"C:\Users\neera\OneDrive\Desktop\pystockapp\cleaned_stock"
MODEL_FOLDER = r"C:\Users\neera\OneDrive\Desktop\pystockapp\models"

# Ensure model folder exists
os.makedirs(MODEL_FOLDER, exist_ok=True)

# List of stock symbols
stock_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BRK.B", "V"]

# Train models for each stock
for stock in stock_symbols:
    file_path = os.path.join(CLEANED_FOLDER, f"{stock}_historical_data.csv")  # ✅ Corrected filename

    if os.path.exists(file_path):
        print(f"✅ Training model for {stock}...")

        # Load CSV file
        df = pd.read_csv(file_path)

        # Auto-fix column names (some APIs may change names)
        df.columns = [col.strip().lower() for col in df.columns]  # Convert to lowercase

        # Rename columns if needed
        column_mapping = {
            "date": "Date",
            "close": "Close",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "volume": "Volume"
        }
        df.rename(columns=column_mapping, inplace=True)

        # Ensure required columns exist
        if "Close" not in df.columns or "Date" not in df.columns:
            print(f"❌ Skipping {stock}: 'Close' or 'Date' column missing!")
            print(f"🔍 Found columns: {df.columns.tolist()}")  # Debugging
            continue

        # Convert Date to datetime & sort
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # Create features (Previous Close, Moving Averages)
        df["Prev_Close"] = df["Close"].shift(1)
        df["MA_55"] = df["Close"].rolling(window=5).mean()
        df["MA_100"] = df["Close"].rolling(window=10).mean()

        # Drop NaN values
        df.dropna(inplace=True)

        # Define features and target
        X = df[["Prev_Close", "MA_55", "MA_100"]]
        y = df["Close"]

        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train AI model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the trained model
        model_filename = os.path.join(MODEL_FOLDER, f"{stock}_model.pkl")
        joblib.dump(model, model_filename)
        print(f"✅ Model saved: {model_filename}")

    else:
        print(f"❌ Data file not found: {file_path}")
