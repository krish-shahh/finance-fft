import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid", font_scale=1.1)
os.makedirs("benchmarks", exist_ok=True)

# Load thread timings
df = pd.read_csv("benchmarks/thread_input_speedups.csv")

# ========================================
# 1. Arithmetic Intensity (Dynamic Based on N)
# ========================================

# Example N values (powers of 2)
N_vals = [2**i for i in range(16, 25)]

# Arithmetic intensity: (FLOPs per element) / (bytes moved per element)
# FFT has ~5N log2(N) FLOPs and ~16N bytes (read + write of complex double)
intensities = [(5 * N * np.log2(N)) / (16 * N) for N in N_vals]  # simplifies to (5 * log2(N)) / 16

plt.figure(figsize=(8, 4))
plt.plot(
    [f"$2^{{{int(np.log2(n))}}}$" for n in N_vals],
    intensities,
    label="Arithmetic Intensity",
    color="firebrick"
)
plt.title("Arithmetic Intensity vs Input Size")
plt.xlabel("Input Size (N)")
plt.ylabel("FLOPs / Byte")
plt.ylim(0, max(intensities) + 0.1)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig("benchmarks/arithmetic_intensity.png")
print("✅ Saved: arithmetic_intensity.png")

# ========================================
# 2. Estimated Memory Traffic
# ========================================
memory_bytes = [16 * N * np.log2(N) for N in N_vals]
memory_gb = np.array(memory_bytes) / (1024**3)

plt.figure(figsize=(8, 4))
plt.plot([f"$2^{{{int(np.log2(n))}}}$" for n in N_vals], memory_gb, marker='o')
plt.title("Estimated Memory Traffic vs Input Size")
plt.xlabel("Input Size (N)")
plt.ylabel("Total Data Moved (GB)")
plt.tight_layout()
plt.savefig("benchmarks/memory_traffic.png")
print("✅ Saved: memory_traffic.png")

# ========================================
# 3. Thread Efficiency
# ========================================
baseline_times = df[df["Threads"] == 1].set_index("N")["Time"]
eff_data = []

for _, row in df.iterrows():
    N = row["N"]
    T = row["Threads"]
    time = row["Time"]
    speedup = baseline_times[N] / time
    efficiency = speedup / T
    eff_data.append({"N": N, "Threads": T, "Efficiency": efficiency})

eff_df = pd.DataFrame(eff_data)
pivot = eff_df.pivot(index="Threads", columns="N", values="Efficiency")

plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="Blues")
plt.title("Thread Efficiency vs Input Size")
plt.xlabel("Input Size (N)")
plt.ylabel("Threads")
plt.tight_layout()
plt.savefig("benchmarks/thread_efficiency_heatmap.png")
print("✅ Saved: thread_efficiency_heatmap.png")
