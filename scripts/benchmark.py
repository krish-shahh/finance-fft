import subprocess
import csv
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

BIN_SERIAL = "./bin/fft_serial"
BIN_PARALLEL = "./bin/fft_parallel"
OUT_CSV = "benchmarks/fft_timings.csv"

input_sizes = [2**k for k in range(10, 25)]  # 2^10 to 2^24

def run_fft(binary, n):
    result = subprocess.run([binary, str(n)], capture_output=True, text=True)
    output = result.stdout.strip().splitlines()
    for line in output:
        if "Time =" in line:
            return float(line.split("Time =")[1].split()[0])
    return None

def benchmark():
    rows = []
    for n in input_sizes:
        print(f"Running N = {n}")
        t_serial = run_fft(BIN_SERIAL, n)
        t_parallel = run_fft(BIN_PARALLEL, n)
        rows.append({"N": n, "serial_time": t_serial, "parallel_time": t_parallel})

    os.makedirs("benchmarks", exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["N", "serial_time", "parallel_time"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Results saved to {OUT_CSV}")
    return pd.DataFrame(rows)

def plot(df):
    df["speedup"] = df["serial_time"] / df["parallel_time"]
    df["N_log2"] = np.log2(df["N"])

    sns.set(style="whitegrid")

    plt.figure()
    sns.lineplot(x="N_log2", y="serial_time", data=df, label="Serial")
    sns.lineplot(x="N_log2", y="parallel_time", data=df, label="Parallel")
    plt.xlabel("log₂(N)")
    plt.ylabel("Runtime (seconds)")
    plt.title("FFT Runtime vs Input Size")
    plt.savefig("benchmarks/runtime_plot.png")

    plt.figure()
    sns.lineplot(x="N_log2", y="speedup", data=df, marker="o")
    plt.xlabel("log₂(N)")
    plt.ylabel("Speedup (Serial / Parallel)")
    plt.title("FFT Speedup vs Input Size")
    plt.savefig("benchmarks/speedup_plot.png")

    print("✅ Plots saved in benchmarks/")

if __name__ == "__main__":
    df = benchmark()
    plot(df)
