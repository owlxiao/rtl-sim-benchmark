from pathlib import Path
import pandas as pd
import os

root = Path(os.getenv('TEST_ROOT'))
results_dir = root.joinpath('results')

to_latex_format = dict(
    label='tab:platform-2',
    caption='Platform Settings 2',
    position='h',
    hrules=True
)

s = pd.read_csv(results_dir.joinpath('platform-info.csv')).style
s.set_table_styles([{'selector': '', 'props': ':small'}])
s.hide(axis='index').to_latex(
    'out/platform-extra-info.tex',
    **to_latex_format
)
