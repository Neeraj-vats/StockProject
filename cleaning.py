import pandas as pd
import numpy as np
import os

# Folder containing uncleaned stock data
folder_path = r"C:\Users\neera\OneDrive\Desktop\pystockapp\uncleaned_stock"

cleaned_folder = r"C:\Users\neera\OneDrive\Desktop\pystockapp\cleaned_stock"  # Folder to save cleaned data

# Ensure cleaned_stock folder exists
os.makedirs(cleaned_folder, exist_ok=True)

# Get list of all CSV files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

for file in files:
    file_path = os.path.join(folder_path, file)

    # Load each CSV file
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # Step 1: Drop duplicate rows (if any)
    df = df.drop_duplicates()

    # Step 2: Handle missing values
    df = df.dropna()  # Removes rows with missing values

    # Step 3: Ensure numeric columns are correct
    df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors="coerce")

    # Step 4: Remove outliers using Z-score
    from scipy.stats import zscore
    z_scores = np.abs(zscore(df[["Open", "High", "Low", "Close", "Volume"]]))
    df = df[(z_scores < 3).all(axis=1)]  # Keeping only data within 3 standard deviations

    # Step 5: Save cleaned data in new folder
    cleaned_file_path = os.path.join(cleaned_folder, file)
    df.to_csv(cleaned_file_path)

    print(f"✅ Cleaned: {file}")

print("🎉 All stock data cleaned & saved in 'cleaned_stock/' folder!")
