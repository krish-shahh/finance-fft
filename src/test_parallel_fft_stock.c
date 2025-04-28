#include "fft.h"
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <omp.h>

#define MAX_LINE_LEN 128

void read_input_from_file(const char *filename, complex double **data, size_t *n) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }

    // Count lines
    size_t count = 0;
    char line[MAX_LINE_LEN];
    while (fgets(line, sizeof(line), fp)) count++;
    rewind(fp);

    *data = malloc(count * sizeof(complex double));
    if (!*data) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }

    for (size_t i = 0; i < count; ++i) {
        double real, imag;
        fscanf(fp, "%lf %lf", &real, &imag);
        (*data)[i] = real + imag * I;
    }

    fclose(fp);
    *n = count;
}

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

int main() {
    complex double *data;
    size_t n;

    read_input_from_file("data/input_fft.txt", &data, &n);

    double start = omp_get_wtime();
    parallel_fft(data, n);
    double end = omp_get_wtime();

    printf("Parallel FFT on stock data complete. N = %zu, Time = %.6f seconds\n", n, end - start);

    write_output_to_file("output/fft_stock_output.txt", data, n);
    free(data);
    return 0;
}
