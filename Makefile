# Makefile for Serial and Parallel FFT

CC = gcc
CFLAGS = -std=c11 -O2 -Wall -Iinclude -fopenmp
LDFLAGS = -lm

SRC_DIR = src
BIN_DIR = bin
OUT_DIR = output
DATA_DIR = data

SERIAL_SRC = $(SRC_DIR)/serial_fft.c $(SRC_DIR)/test_serial_fft.c
PARALLEL_SRC = $(SRC_DIR)/parallel_fft.c $(SRC_DIR)/test_parallel_fft.c
STOCK_SRC = $(SRC_DIR)/parallel_fft.c $(SRC_DIR)/test_parallel_fft_stock.c

SERIAL_BIN = $(BIN_DIR)/fft_serial
PARALLEL_BIN = $(BIN_DIR)/fft_parallel
STOCK_BIN = $(BIN_DIR)/fft_stock

.PHONY: all run run-parallel run-stock validate clean dirs

all: dirs $(SERIAL_BIN) $(PARALLEL_BIN) $(STOCK_BIN)

dirs:
	mkdir -p $(BIN_DIR) $(OUT_DIR)

$(SERIAL_BIN): $(SERIAL_SRC)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

$(PARALLEL_BIN): $(PARALLEL_SRC)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

$(STOCK_BIN): $(STOCK_SRC)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

run: $(SERIAL_BIN)
	$(SERIAL_BIN)
	mv -f output_fft.txt $(OUT_DIR)/output_fft.txt

run-parallel: $(PARALLEL_BIN)
	$(PARALLEL_BIN)
	mv -f output_fft_parallel.txt $(OUT_DIR)/output_fft_parallel.txt

run-stock: $(STOCK_BIN)
	$(STOCK_BIN)

validate: run run-parallel
	python3 scripts/validate_fft.py

clean:
	rm -rf $(BIN_DIR) $(OUT_DIR)
