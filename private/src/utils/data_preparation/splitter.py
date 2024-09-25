import pandas as pd

def splitter(raw_data):
    return pd.Series(raw_data.split('|_|', 1))