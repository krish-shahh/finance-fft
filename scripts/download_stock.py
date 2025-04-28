import yfinance as yf
import pandas as pd
import os

def download_stock(symbol="AAPL", period="5y", save_dir="data"):
    os.makedirs(save_dir, exist_ok=True)
    df = yf.download(symbol, period=period)
    csv_path = os.path.join(save_dir, f"{symbol}.csv")
    df.to_csv(csv_path)
    print(f"✅ Downloaded {symbol} data to {csv_path}")

if __name__ == "__main__":
    download_stock("AAPL")  # or "SPY", "TSLA", etc.
    download_stock("SPY")
