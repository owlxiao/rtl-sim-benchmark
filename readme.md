# RTL Simulation Benchmark

This repository is designed to test the performance of RTL simulators.

## Setup

Use the `env.py` script to check if the environment is properly installed.


```bash
$ python env.py
```

## Evaluation


Build the executable:

```bash
$ make build
```

Run the executable:


```bash
$ make run
```

The collected data is listed in `results` folder, like this:

```bash
$ tree -L 1 results
results
├── benchmark-info.json
├── cpu-info.json
├── platform-info.csv
├── result.csv
└── runs
```

## Generate Report

Run the following command to generate a performance report(report.pdf)

```bash
make report
```

The `results` folder contains an [example report](results/report.pdf) named `example-report.pdf`.