import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_log_returns(symbol):
    df = pd.read_csv(f"data/{symbol}.csv", skiprows=3, names=["Date", "Close", "High", "Low", "Open", "Volume"])
    close = pd.to_numeric(df["Close"], errors="coerce").dropna()
    log_returns = np.diff(np.log(close.values))
    N = 2 ** int(np.floor(np.log2(len(log_returns))))
    return log_returns[:N]

def plot_comparison():
    sns.set(style="whitegrid")
    aapl = load_log_returns("AAPL")
    spy = load_log_returns("SPY")

    fft_aapl = np.fft.fft(aapl)
    fft_spy = np.fft.fft(spy)

    power_aapl = np.abs(fft_aapl[:len(fft_aapl)//2])**2
    power_spy = np.abs(fft_spy[:len(fft_spy)//2])**2
    freqs = np.fft.fftfreq(len(fft_aapl))[:len(fft_aapl)//2]

    plt.figure(figsize=(10, 5))
    plt.plot(freqs, power_aapl, label="AAPL", linewidth=1.5)
    plt.plot(freqs, power_spy, label="SPY", linewidth=1.5)
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.title("Power Spectrum Comparison: AAPL vs SPY Log Returns")
    plt.legend()
    plt.tight_layout()
    plt.savefig("benchmarks/aapl_vs_spy_spectrum.png")
    print("✅ Saved: benchmarks/aapl_vs_spy_spectrum.png")

if __name__ == "__main__":
    plot_comparison()
