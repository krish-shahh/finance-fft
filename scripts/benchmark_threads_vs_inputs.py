import subprocess
import time
import csv
import os

bin_path = "./bin/fft_parallel"
log_file = "benchmarks/thread_input_speedups.csv"

# Powers of 2: 2^16 to 2^24
input_sizes = [2**i for i in range(16, 25)]
thread_counts = [1, 2, 4, 8, 16, 32, 64, 128]

results = []

print("Running parallel FFT benchmark across N and thread counts...\n")

for N in input_sizes:
    for threads in thread_counts:
        env = os.environ.copy()
        env["OMP_NUM_THREADS"] = str(threads)
        print(f"Running: N={N}, Threads={threads}")

        try:
            start = time.time()
            proc = subprocess.run([bin_path, str(N)],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  universal_newlines=True,
                                  env=env,
                                  timeout=20)
            end = time.time()

            output = proc.stdout
            runtime_line = [line for line in output.splitlines() if "Time" in line]
            if runtime_line:
                runtime = float(runtime_line[0].split("=")[-1].strip().split()[0])
            else:
                runtime = end - start  # fallback

            results.append([N, threads, runtime])
        except subprocess.TimeoutExpired:
            print(f"Timeout: N={N}, Threads={threads}")
            results.append([N, threads, "timeout"])

# Save results
os.makedirs("benchmarks", exist_ok=True)
with open(log_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["N", "Threads", "Time"])
    writer.writerows(results)

print(f"\n✅ Benchmark complete. Results saved to {log_file}")
