from pathlib import Path
import pandas as pd
import json
import os
import re

root = Path(os.getenv('TEST_ROOT'))
results_dir = root.joinpath('results')


def clean_value(s):
    s = re.sub(r'\(\d instances?\)', '', s)
    s = re.sub(r'\d-Core Processor', '', s)
    s = re.sub(r'with.*', '', s)
    s = re.sub(r'Intel\(R\) Core\(TM\)|AMD', '', s)
    s = re.sub(r'Ryzen \d', r'Ryzen', s)
    s = re.sub(r'CPU @ [0-9.]+GHz', '', s)
    s = re.sub(r'(\d\d\d\d).\d\d\d\d', r'\1 MHz', s)
    return s.strip()


cpu_info = json.loads(results_dir.joinpath('cpu-info.json').read_text())
index = [x['field'].strip().rstrip(':') for x in cpu_info['lscpu']]
value = [x['data'].strip() for x in cpu_info['lscpu']]
ser = pd.Series(value, index=index)
ser = ser[['Model name', 'CPU max MHz', 'L1d cache',
           'L1i cache', 'L2 cache', 'L3 cache']]
ser.index = ['CPU', 'Max Frequency', 'L1i', 'L1d', 'L2', 'L3']
ser = ser.apply(clean_value)
cpuinfo = ser

to_latex_format = dict(
    label='tab:platform-1',
    caption='Platform Settings 1',
    position='h!',
    hrules=True
)

s = pd.DataFrame(cpuinfo).T.style
s.set_table_styles([{'selector': '', 'props': ':small'}])
s.to_latex(
    'out/platform-info.tex',
    **to_latex_format
)
