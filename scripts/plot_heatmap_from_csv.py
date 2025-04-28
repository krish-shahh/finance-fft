import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load benchmark data
df = pd.read_csv("benchmarks/thread_input_speedups.csv")

# Pivot to get Time[N][Threads]
pivot = df.pivot(index="N", columns="Threads", values="Time")
pivot = pivot.sort_index()

# Normalize to 1-thread time per input size
speedup = pivot.apply(lambda col: pivot[1] / col)

# Plot
plt.figure(figsize=(10, 6))
sns.heatmap(speedup, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.3)

plt.title("Parallel FFT Speedup vs Input Size and Threads")
plt.xlabel("Threads")
plt.ylabel("Input Size (N)")
plt.tight_layout()

# Save
os.makedirs("benchmarks", exist_ok=True)
plt.savefig("benchmarks/thread_input_heatmap.png")
print("✅ Saved heatmap to benchmarks/thread_input_heatmap.png")
