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

def convert_time_dask(df,rounding=None):
    df["date"] = dd.to_datetime(df["xltime"], unit="d", origin="1899-12-30", utc=True)
    if rounding:
        df["date"] = df["date"].round(rounding)
    return df


def log_returns(x: pd.Series):
    ret = np.log(x).diff().dropna()
    return ret

def returns(x:pd.Series):
    return x.pct_change().dropna()

def price_difference(x: pd.Series):
    return x.diff().dropna()

def binary_returns(x: pd.Series):
    ret = x.diff(1).dropna() > 0
    return ret*1-1*(1-ret)

def resample(x: pd.Series):
    return x.resample("1S").mean().dropna()


def moving_average(x: pd.Series, w=30):
    return x.rolling(w, min_periods=1).mean()

def replace_inf(df):
    df.replace([np.inf, -np.inf], np.nan).dropna()
 
def __to_numeric(x,module,col="price"):
    x[col] = module.to_numeric(x[col], errors="coerce")
    return x.dropna()

def to_numeric(x: pd.Series,col="price"):
    x[col] = pd.to_numeric(x[col], errors="coerce")
    return x.dropna()
    #return __to_numeric(x,pd)

def to_numeric_dask(x,col="price"):
    return __to_numeric(x,dd,col)

#############################################################
################### Pipeline transformations ##############
#############################################################

transformations = {
    'returns':returns,
    'price_difference': price_difference,
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
