import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_fft_output(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return np.array([float(r) + 1j * float(i) for r, i in (line.strip().split() for line in lines)])

def load_log_returns(csv_path):
    df = pd.read_csv(csv_path, skiprows=3, names=["Date", "Close", "High", "Low", "Open", "Volume"])
    close = pd.to_numeric(df["Close"], errors="coerce").dropna()
    log_returns = np.diff(np.log(close.values))
    N = 2 ** int(np.floor(np.log2(len(log_returns))))
    return log_returns[:N]

def compare_fft_power():
    sns.set(style="whitegrid")
    c_fft = load_fft_output("output/fft_stock_output.txt")
    py_input = load_log_returns("data/AAPL.csv")
    py_fft = np.fft.fft(py_input)

    N = len(c_fft)
    freqs = np.fft.fftfreq(N)

    df = pd.DataFrame({
        "Frequency": freqs[:N//2],
        "Power (C FFT)": np.abs(c_fft[:N//2])**2,
        "Power (NumPy FFT)": np.abs(py_fft[:N//2])**2
    })

    plt.figure(figsize=(10, 5))
    sns.lineplot(x="Frequency", y="Power (C FFT)", data=df, label="C FFT", linewidth=1.5)
    sns.lineplot(x="Frequency", y="Power (NumPy FFT)", data=df, label="NumPy FFT", linewidth=1.5)
    plt.title("Power Spectrum: C vs NumPy FFT")
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.legend()
    plt.tight_layout()
    plt.savefig("benchmarks/fft_comparison.png")
    print("✅ Overlay plot saved to benchmarks/fft_comparison.png")

if __name__ == "__main__":
    compare_fft_power()
