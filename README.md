# High-Performance Iterative FFT with Financial Application

## Overview
This project implements a **high-performance, radix-2 iterative Fast Fourier Transform (FFT)** from scratch in C, parallelized using **OpenMP** and scaled up to \(2^{24}\) elements.  
We apply this FFT to **real financial data (AAPL and SPY log returns)** and analyze performance using techniques like **roofline modeling**, **memory behavior analysis**, and **thread scaling**.

## Key Features
- **Iterative radix-2 Cooley-Tukey FFT** (avoiding recursion)
- **Parallelization** using OpenMP (`#pragma omp parallel for`)
- **Optimizations**:
  - In-place memory layout
  - Loop fusion for butterfly updates
  - Thread-private variables to avoid false sharing
- **Validation** against NumPy's `numpy.fft.fft()` (relative error < \(10^{-11}\))
- **Performance analysis**: speedup, memory bandwidth, roofline modeling
- **Financial signal analysis**: frequency domain insights into AAPL vs SPY

## Performance Highlights
- Achieved up to **8.3× speedup** over serial on **128 threads**
- Scaling limited by **memory bandwidth** beyond 32 threads
- Real hardware counters confirm **memory-bound behavior**

## Experimental Setup
- System: BU SCC (Intel Xeon Gold 6248, Cascade Lake)
- Compiler: GCC with `-fopenmp -O3`
- Input sizes: \(2^{16}\) to \(2^{24}\)
- Timing: `omp_get_wtime()`

## Financial Analysis
- Downloaded 5 years of **AAPL** and **SPY** data using `yfinance`
- Computed **log returns** and fed into FFT
- **Power spectrum comparison** shows AAPL has more high-frequency content (greater short-term volatility) than SPY.

## How to Build and Run
```bash
# Clone the repository
git clone https://github.com/krish-shahh/finance-fft
cd finance-fft

# Build everything
make

# Validate serial and parallel FFT correctness
make validate

# Run FFT on stock data
make run -stock
python3 scripts/compare_fft_power.py

# Benchmark thread scaling
python3 scripts/benchmark_threads_vs_inputs.py
python3 scripts/plot_heatmap_from_csv.py

# Model memory behavior
python3 scripts/model_memory_behavior.py

# Plot roofline (requires manual perf data collection)
python3 scripts/plot_roofline_fft.py
```

## Future Work
- Implement SIMD butterfly kernels (AVX2 intrinsics)
- Develop cache-blocked FFTs with loop tiling
- Add NUMA-aware thread binding and memory allocation
- Real-time FFT streaming from live stock APIs
- Integrate FFT output into financial ML models (GARCH, HMMs)

## Repository
🔗 [GitHub: finance-fft](https://github.com/krish-shahh/finance-fft)
