import pandas as pd
import numpy as np
import os

def export_log_returns(csv_path="data/AAPL.csv", out_path="data/input_fft.txt"):
    df = pd.read_csv(csv_path, skiprows=3, names=["Date", "Close", "High", "Low", "Open", "Volume"])
    close = pd.to_numeric(df["Close"], errors="coerce").dropna()

    log_returns = np.diff(np.log(close.values))
    N = 2 ** int(np.floor(np.log2(len(log_returns))))
    log_returns = log_returns[:N]

    os.makedirs("data", exist_ok=True)
    with open(out_path, "w") as f:
        for x in log_returns:
            f.write(f"{x:.10f} 0.0\n")  # real imag

    print(f"✅ Exported {N} log return values to {out_path}")

if __name__ == "__main__":
    export_log_returns()
