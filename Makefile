export RUNS = verilator-1
export TEST_ROOT = $(shell pwd)

build:
	make -C runs build

run:
	python tools/benchmark.py