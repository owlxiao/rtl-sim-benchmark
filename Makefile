export RUNS = verilator-1 verilator-2 arcilator essent
export TEST_ROOT = $(shell pwd)

build:
	make -C runs build

clean-build:
	make -C runs clean

clean-report:
	make -C tools/analysis clean

clean-results:
	rm -rf results/*.json results/*.csv

run:
	python tools/benchmark.py

results/platform-info.csv:
	python tools/collect-info.py > $@

results/cpu-info.json:
	lscpu -J > $@

results/benchmark-info.json:
	cp cases/benchmark-info.json $@

report: results/platform-info.csv results/cpu-info.json results/benchmark-info.json
	make -j -C tools/analysis

	cp tools/analysis/report/report.pdf $(TEST_ROOT)/results/report.pdf