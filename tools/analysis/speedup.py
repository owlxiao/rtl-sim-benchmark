import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from pathlib import Path
import os

baseline_name = 'verilator-1'


def make_plot(df: pd.DataFrame):
    df['speed'] = df['sim-cycles'] / df['time']

    piv = df.pivot_table(
        values='speed', index='benchmark', columns='simulator')

    baseline = piv[baseline_name].copy()

    for col in piv:
        piv[col] /= baseline

    piv = piv.stack().reset_index(name='speedup')

    plt.figure(figsize=(6, 3))
    bar = sns.barplot(
        data=piv,
        x='benchmark', y='speedup',
        hue='simulator',
        palette='muted'
    )

    sns.despine()
    plt.tight_layout()
    plt.savefig('out/speedup.pdf')


if __name__ == '__main__':
    root = Path(os.getenv('TEST_ROOT'))
    results_dir = root.joinpath('results')

    make_plot(pd.read_csv((results_dir.joinpath("result.csv"))))
