import pandas as pd


def convert_time(df):
    df["date"] = pd.to_datetime(
        df["xltime"], unit="d", origin="1899-12-30", utc=True)
    return df


def transform_to_returns(x):
    ret = x.diff(1).dropna() > 0
    return ret*1-1*(1-ret)
