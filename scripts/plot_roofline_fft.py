import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ======================================
# Constants
# ======================================
peak_gflops = 1000  # estimated peak GFLOPs on BU SCC node
peak_bandwidth = 100  # GB/s

# FFT input
N = 2**24
log2N = np.log2(N)
flops = 5 * N * log2N
total_bytes = 2 * N * 16  # load + store complex double

# FFT timing from your OpenMP timing
runtime_omp = 2.85  # seconds

# FFT from perf (effective bandwidth)
runtime_perf = 2.85  # same, since perf ran the same FFT
measured_bandwidth = total_bytes / runtime_perf / 1e9  # GB/s
measured_gflops = flops / runtime_perf / 1e9  # GFLOPs

# Compute arithmetic intensity
intensity_fft = flops / total_bytes  # ~5 log2N / 16

# ======================================
# Roofline Curve
# ======================================
intensity_range = np.logspace(-1, 2, 200)
roofline = np.minimum(peak_gflops, peak_bandwidth * intensity_range)

# ======================================
# Plot
# ======================================
plt.figure(figsize=(8, 6))
plt.loglog(intensity_range, roofline, label="Roofline Bound", color="black", linewidth=2)

# Plot FFT ideal
plt.scatter(intensity_fft, measured_gflops, color="crimson", label="FFT (128 threads)", s=70, zorder=5)
plt.axvline(intensity_fft, color='crimson', linestyle='--', linewidth=0.8)
plt.axhline(measured_gflops, color='crimson', linestyle='--', linewidth=0.8)

# Annotate
plt.annotate("FFT\n(2²⁴)", (intensity_fft * 1.1, measured_gflops * 0.8), fontsize=10, color="crimson")

# Labels and formatting
plt.xlabel("Arithmetic Intensity (FLOPs / Byte)")
plt.ylabel("Performance (GFLOPs/sec)")
plt.title("Roofline Model: FFT Performance (N = $2^{24}$, 128 Threads)")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("benchmarks/roofline_fft.png")
print("✅ Saved: benchmarks/roofline_fft.png")
