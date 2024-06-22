export RUNS = verilator-1
export TEST_ROOT = $(shell pwd)

build:
	make -C runs build

run:
	python tools/benchmark.py

results/platform-info.csv:
	python tools/collect-info.py > $@

results/cpu-info.json:
	lscpu -J > $@

report: results/platform-info.csv results/cpu-info.json
	make -j -C tools/analysis

	cp tools/analysis/report/report.pdf $(TEST_ROOT)/results/report.pdf