import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_stock_close_prices(csv_path):
    # Skip metadata rows and assign proper headers
    df = pd.read_csv(csv_path, skiprows=3, names=["Date", "Close", "High", "Low", "Open", "Volume"])

    # Ensure Close column is numeric
    close = pd.to_numeric(df["Close"], errors="coerce").dropna()

    # Trim to nearest power of 2
    N = 2 ** int(np.floor(np.log2(len(close))))
    return close.values[:N]

def plot_power_spectrum(signal, fs=1.0, title="Power Spectrum"):
    sns.set(style="whitegrid", font_scale=1.1)

    N = len(signal)
    fft_vals = np.fft.fft(signal)
    power = np.abs(fft_vals) ** 2
    freqs = np.fft.fftfreq(N, d=1/fs)

    df = pd.DataFrame({
        "Frequency": freqs[:N//2],
        "Power": power[:N//2]
    })

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x="Frequency", y="Power", linewidth=1.5)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectrum")
    plt.tight_layout()
    plt.savefig("benchmarks/power_spectrum.png")
    print("✅ Power spectrum saved to benchmarks/power_spectrum.png")

if __name__ == "__main__":
    data = load_stock_close_prices("data/AAPL.csv")
    plot_power_spectrum(data, fs=1.0, title="AAPL Power Spectrum")
