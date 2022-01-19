import pandas as pd
import numpy as np

def convert_time(df):
    df["date"] = pd.to_datetime(
        df["xltime"], unit="d", origin="1899-12-30", utc=True)
    return df


def transform_to_returns(x):
    ret = np.log(x).diff(1).dropna()
    return ret


def transform_to_bin_ret(x):
    ret = x.diff(1).dropna() > 0
    return ret*1-1*(1-ret)