import subprocess
import csv
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

N = 2**24
binary = "./bin/fft_parallel"
output_csv = "benchmarks/thread_scaling.csv"
threads_list = [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 96, 112, 128]

def run_fft_with_threads(n_threads):
    result = subprocess.run(
        ["bash", "-c", f"OMP_NUM_THREADS={n_threads} {binary} {N}"],
        capture_output=True, text=True
    )
    for line in result.stdout.strip().splitlines():
        if "Time =" in line:
            return float(line.split("Time =")[1].split()[0])
    return None

def benchmark():
    os.makedirs("benchmarks", exist_ok=True)
    rows = []
    for t in threads_list:
        print(f"Running with {t} thread(s)...")
        time = run_fft_with_threads(t)
        rows.append({"threads": t, "time": time})

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["threads", "time"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Results saved to {output_csv}")
    return pd.DataFrame(rows)

def plot(df):
    df["speedup"] = df["time"].iloc[0] / df["time"]  # relative to 1-thread time

    sns.set(style="whitegrid")

    plt.figure()
    sns.lineplot(x="threads", y="time", data=df, marker="o")
    plt.title("Parallel FFT Runtime vs Threads")
    plt.xlabel("Threads")
    plt.ylabel("Time (seconds)")
    plt.savefig("benchmarks/thread_runtime.png")

    plt.figure()
    sns.lineplot(x="threads", y="speedup", data=df, marker="o")
    plt.title("Parallel FFT Speedup vs Threads")
    plt.xlabel("Threads")
    plt.ylabel("Speedup (relative to 1 thread)")
    plt.savefig("benchmarks/thread_speedup.png")

    print("✅ Plots saved to benchmarks/")

if __name__ == "__main__":
    df = benchmark()
    plot(df)
