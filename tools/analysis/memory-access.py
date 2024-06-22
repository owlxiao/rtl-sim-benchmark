from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import gmean
from matplotlib import ticker
import seaborn as sns
import pandas as pd

import os

root = Path(os.getenv('TEST_ROOT'))
results_dir = root.joinpath('results')


df = pd.read_csv((results_dir.joinpath("result.csv")))
df['access_ratio'] = (df['cpu_core/L1-dcache-loads/'] +
                      df['cpu_core/L1-dcache-stores/']) / df['cpu_core/instructions/']

df = df.set_index('simulator').loc['verilator-1']
df['type'] = 'normal'
df.loc[len(df)] = pd.Series(
    {'benchmark': 'Average', 'type': 'avg', 'access_ratio': gmean(df['access_ratio'])})
palette = sns.color_palette('muted')


plt.figure(figsize=(6, 3))
palette = sns.color_palette('muted')
bar = sns.barplot(data=df, x='benchmark', y='access_ratio',
                  errwidth=0, palette=palette)
bar.patches[-1].set_facecolor(palette[1])
plt.xticks(rotation=-30, ha='left')
sns.despine()
plt.ylabel('Mem. Access Instructions (%)')
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

plt.tight_layout()
plt.savefig('out/memory-access.pdf')
