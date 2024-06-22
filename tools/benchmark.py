from pathlib import Path

import subprocess
import json

from tqdm import tqdm
import pandas as pd

from perflib import *

root = Path('.')
runs_dir = root.joinpath('runs')
results_dir = root.joinpath('results')


tasksets = {
    'verilator-1': 'taskset -c 1'
}

benchmarks = [f.stem for f in root.joinpath('cases').glob('*.fir')]


def run_task(bench: str, sim: str, exe: Path, taskset: str,  results_dir: Path, runs: int, cycles: int):
    if not exe.exists():
        print(f"{exe} not found")
        return

    res = results_dir.joinpath(f"{bench}-{sim}.json")

    run_data = []

    perf_command = make_perf_command()

    with tqdm(total=runs, desc=f'Initial setup for {bench}-{sim}') as pbar:
        for run in range(runs):
            run_field = {
                'simulator': sim,
                'benchmark': bench,
                'sim-cycles': cycles,
                'run': run
            }

            pbar.set_description(
                f"Running {bench}-{sim} simulation, run {run + 1}/{runs}")

            cmd_line = f"{taskset} {perf_command} {exe} {cycles}"
            proc = subprocess.Popen(cmd_line, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=True)
            stdout, stderr = proc.communicate()
            perf = stderr.decode()

            try:
                tm = int(stdout.decode())
            except ValueError:
                print("ERROR: Failed to decode output for command:", cmd_line)
                exit(1)

            run_field['time'] = tm

            perf = parse_perf(perf)

            if perf is not None:
                run_field.update(perf)
                run_data.append(run_field)

            pbar.update(1)

    with res.open('w') as f:
        f.write(json.dumps(run_data, indent=2))


results_dir.mkdir(exist_ok=True, parents=True)

for bench in benchmarks:
    sim = 'verilator-1'
    run_task(bench=bench, sim=sim, exe=runs_dir.joinpath(
        sim, 'bin', bench + '.out'),
        taskset=tasksets[sim],
        results_dir=results_dir,
        runs=10,
        cycles=500000
    )

df = []
for res in results_dir.glob("*.json"):
    with res.open() as f:
        df += json.load(f)
pd.DataFrame(df).to_csv(root.joinpath('results', 'result.csv'), index=False)
