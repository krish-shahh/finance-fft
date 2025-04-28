// serial_fft.c
#include "fft.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

static size_t reverse_bits(size_t x, unsigned int bits) {
    size_t result = 0;
    for (unsigned int i = 0; i < bits; ++i) {
        result <<= 1;
        result |= (x & 1);
        x >>= 1;
    }
    return result;
}

void serial_fft(complex double *data, size_t n) {
    if ((n & (n - 1)) != 0) {
        fprintf(stderr, "Input size must be a power of 2\n");
        exit(EXIT_FAILURE);
    }

    unsigned int log_n = 0;
    for (size_t tmp = n; tmp > 1; tmp >>= 1)
        log_n++;

    // Bit-reversal permutation
    for (size_t i = 0; i < n; ++i) {
        size_t j = reverse_bits(i, log_n);
        if (j > i) {
            complex double tmp = data[i];
            data[i] = data[j];
            data[j] = tmp;
        }
    }

    // Iterative FFT
    for (size_t s = 1; s <= log_n; ++s) {
        size_t m = 1 << s;
        complex double wm = cexp(-2.0 * I * M_PI / m);
        for (size_t k = 0; k < n; k += m) {
            complex double w = 1.0;
            for (size_t j = 0; j < m / 2; ++j) {
                complex double t = w * data[k + j + m / 2];
                complex double u = data[k + j];
                data[k + j] = u + t;
                data[k + j + m / 2] = u - t;
                w *= wm;
            }
        }
    }
}
