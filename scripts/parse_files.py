"""
A helper script for parsing csv files.
"""

import os
import pandas as pd

def parse_files(path):
    csv_files = [file for file in os.listdir(path) if file.endswith('.csv')]

    dfs = []
    for file in csv_files:
        df = pd.read_csv(os.path.join(path, file))
        dfs.append(df)
    
    df = pd.concat(dfs, ignore_index=True)
    
    return df