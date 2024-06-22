from pathlib import Path
import pandas as pd
import json
import os

root = Path(os.getenv('TEST_ROOT') or '.')
results_dir = root.joinpath('results')

with results_dir.joinpath('benchmark-info.json').open('r') as file:
    benchmarks = json.load(file)

rows = []
for entry in benchmarks:
    category = entry['category']
    for bm in entry['benchmarks']:
        rows.append({
            'Category': category,
            'Benchmark Name': bm['name'],
            'Description': bm['description'],
            'Source': bm['source']
        })

df = pd.DataFrame(rows)

latex_format = {
    'label': 'tab:benchmarks',
    'caption': 'Benchmarks used',
    'position': 'h',
    'hrules': True,
}

styler = df.style
styler.set_table_styles([{'selector': '', 'props': ':small'}])
styler.to_latex('out/benchmark-info.tex', **latex_format)
