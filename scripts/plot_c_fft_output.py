import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def load_fft_output(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return np.array([float(r) + 1j * float(i) for r, i in (line.strip().split() for line in lines)])

def plot_power_spectrum_from_c(filename, title="C FFT Power Spectrum"):
    data = load_fft_output(filename)
    power = np.abs(data)**2
    N = len(power)
    freqs = np.fft.fftfreq(N, d=1.0)

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 5))
    df = pd.DataFrame({
        "Frequency": freqs[:N//2],
        "Power": power[:N//2]
    })
    sns.lineplot(data=df, x="Frequency", y="Power", linewidth=1.5)
    plt.title(title)
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.tight_layout()
    plt.savefig("benchmarks/c_fft_power_spectrum.png")
    print("✅ Plot saved to benchmarks/c_fft_power_spectrum.png")

if __name__ == "__main__":
    plot_power_spectrum_from_c("output/fft_stock_output.txt")
