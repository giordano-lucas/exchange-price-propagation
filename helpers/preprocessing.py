import pandas as pd
import numpy as np
import dask.dataframe as dd

#############################################################
################### Individual transformations ##############
#############################################################

def convert_time(df):
    df["date"] = pd.to_datetime(
        df["xltime"], unit="d", origin="1899-12-30", utc=True)
    return df

def log_returns(x: pd.Series):
    ret = np.log(x).diff().dropna()
    return ret

def returns(x:pd.Series):
    return x.pct_change().dropna()

def binary_returns(x: pd.Series):
    ret = x.diff(1).dropna() > 0
    return ret*1-1*(1-ret)

def resample(x: pd.Series):
    return x.resample("1S").mean().dropna()


def moving_average(x: pd.Series, w=30):
    return x.rolling(w, min_periods=1).mean()

def replace_inf(df):
    df.replace([np.inf, -np.inf], np.nan).dropna()
 
def __to_numeric(x,module):
    x.price = module.to_numeric(x.price, errors="coerce")
    return x.dropna()

def to_numeric(x: pd.Series):
    return __to_numeric(x,pd)

def to_numeric_dask(x):
    return __to_numeric(x,dd)

#############################################################
################### Pipeline transformations ##############
#############################################################

transformations = {
    'returns':returns,
    'log_returns': log_returns,
    'binary_returns': binary_returns,
    'moving_average': moving_average,
    'resample': resample,
    'numeric': to_numeric
}

def preprocessing_pipeline(x: pd.Series, steps:list = []):
    for s in steps:
        x = transformations[s](x)
    return x
