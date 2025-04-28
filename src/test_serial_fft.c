#include "fft.h"
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <omp.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

void write_output_to_file(const char *filename, complex double *data, size_t n) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }
    for (size_t i = 0; i < n; ++i) {
        fprintf(fp, "%.10f %.10f\n", creal(data[i]), cimag(data[i]));
    }
    fclose(fp);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <N = 2^k>\n", argv[0]);
        return 1;
    }

    size_t n = atoi(argv[1]);
    if ((n & (n - 1)) != 0) {
        fprintf(stderr, "Error: N must be a power of 2.\n");
        return 1;
    }

    complex double *data = malloc(n * sizeof(complex double));
    if (!data) {
        perror("malloc");
        return 1;
    }

    // Example input: sine wave
    for (size_t i = 0; i < n; ++i) {
        data[i] = sin(2 * M_PI * i / n) + 0.0 * I;
    }

    double start = omp_get_wtime();
    serial_fft(data, n);
    double end = omp_get_wtime();

    write_output_to_file("output_fft.txt", data, n);
    printf("Serial FFT complete. N = %zu, Time = %.6f seconds\n", n, end - start);

    free(data);
    return 0;
}
