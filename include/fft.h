// fft.h
#ifndef FFT_H
#define FFT_H

#include <complex.h>
#include <stddef.h>

// In-place iterative radix-2 Cooley-Tukey FFT
void serial_fft(complex double *data, size_t n);
void parallel_fft(complex double *data, size_t n);

#endif // FFT_H
