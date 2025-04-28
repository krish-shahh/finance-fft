# scripts/validate_fft.py
import numpy as np
import os

def load_fft_output(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return np.array([float(r) + 1j * float(i) for r, i in (line.strip().split() for line in lines)])

def validate(filename, label):
    print(f"\n--- {label} ---")
    output_path = os.path.join("output", filename)  # <-- fixed path
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"{label} output missing: {output_path}")

    input_data = np.array([1, 1, 1, 1, 0, 0, 0, 0], dtype=complex)
    np_fft = np.fft.fft(input_data)
    c_fft = load_fft_output(output_path)

    print("NumPy FFT:")
    print(np_fft)
    print("\nC FFT Output:")
    print(c_fft)

    diff = np.abs(np_fft - c_fft)
    print(f"\nMax difference: {np.max(diff)}")
    assert np.allclose(np_fft, c_fft, atol=1e-6), f"{label} mismatch!"
    print(f"✅ {label} FFT validated successfully.")

if __name__ == "__main__":
    validate("output_fft.txt", "Serial")
    validate("output_fft_parallel.txt", "Parallel")
