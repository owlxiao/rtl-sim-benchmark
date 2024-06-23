import pandas as pd
from pandas.io.formats.style import Styler
from pathlib import Path

import os


def make_latex_table(tab: pd.DataFrame) -> Styler:
    tab.index.name = None
    tab = tab.style

    tab.set_table_styles([{'selector': '', 'props': ':small'}])
    tab = tab.applymap_index(lambda x: 'textbf:--rwrap', 1)

    return tab


def make_table(df: pd.DataFrame, field, highlight) -> Styler:
    df['IPC'] = df['cpu_core/instructions/'] / df['cpu_core/cycles/']

    piv = df.pivot_table(field, index='benchmark', columns='simulator')
    piv_s = make_latex_table(piv)

    piv_s = piv_s.highlight_max(axis=1, color='green', props='textbf:--rwrap')

    return piv_s


if __name__ == '__main__':
    root = Path(os.getenv('TEST_ROOT'))
    results_dir = root.joinpath('results')

    to_latex_format = dict(
        label='tab:ipc',
        caption='Instructions Per Cycle',
        position='h!',
        position_float='centering',
        hrules=True
    )

    make_table(pd.read_csv((results_dir.joinpath("result.csv"))), 'IPC', 'max').to_latex(
        'out/ipc.tex',
        **to_latex_format
    )
