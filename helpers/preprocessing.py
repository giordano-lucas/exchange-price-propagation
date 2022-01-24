import pandas as pd
import numpy as np


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

def binary_returns(x: pd.Series):
    ret = x.diff(1).dropna() > 0
    return ret*1-1*(1-ret)

def resample(x: pd.Series):
    return x.resample("180S").mean()


def moving_average(x: pd.Series, w=30):
    return x.rolling(w, min_periods=1).mean()

def numeric(x: pd.Series):
    return pd.to_numeric(x, errors="coerce").dropna()

#############################################################
################### Pipeline transformations ##############
#############################################################

transformations = {
    'log_returns': log_returns,
    'binary_returns': binary_returns,
    'moving_average': moving_average,
    'resample': resample,
    'numeric': numeric
}

def preprocessing_pipeline(x: pd.Series, steps:list = []):
    for s in steps:
        x = transformations[s](x)
    return x
