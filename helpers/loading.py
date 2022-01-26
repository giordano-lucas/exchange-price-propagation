from helpers import config
import glob
import re
import numpy as np
import pandas as pd

from .preprocessing import *
import traceback

def file_exist(path):
    return len(glob.glob(path)) > 0

# *****************************************************
# ******************** DAILY **************************
# *****************************************************

def __format_loaded_df(df, col, preprocessing_steps):
    df = df.rename(columns={col: "price"})
    series = df[["price", "date"]].drop_duplicates().set_index("date")
    series = series[~series.index.duplicated(keep='first')]
    series = preprocessing_pipeline(
            series,steps=preprocessing_steps )
    series = series.replace([np.inf, -np.inf], np.nan).dropna()
    series = series[np.abs(series.price) > 0.0]
    return series


def __load_bbo_file(file, preprocessing_steps):
    res = pd.read_parquet(file).rename(
        columns={"bid-price": "bid", "ask-price": "ask"})
    res = convert_time(res)
    res = to_numeric(res,col="bid")
    res = to_numeric(res,col="ask")
    res["mid"] = (res.bid + res.ask)/2
    return __format_loaded_df(res, "mid", preprocessing_steps)


def __load_trade_file(file, preprocessing_steps):
    res = pd.read_parquet(file)
    res = convert_time(res)
    res = res[res["trade-stringflag"] == "uncategorized"]
    return __format_loaded_df(res, "trade-price", preprocessing_steps)

def __get_load_file():
    if config['signal'] == 'trade':
        return __load_trade_file
    else:
        return __load_bbo_file

 
   
def load_daily_data(date, preprocessing_steps):
    daily_data = {}
    for market in config['markets']['list']:
        mkt_suffix = config["markets"]['suffix'][market]
        path_expr = f"{config['dir']['data']}/{market}/{config['signal']}/{config['stock']}.{mkt_suffix}/{date}*"
        path = glob.glob(path_expr)
        if len(path) == 0:
            print(f"missing data : {date} {market}", end="\r")
            return
        else:
            path = path[0]
            daily_data[market] = __get_load_file()(path, preprocessing_steps)
 
    return daily_data


# *****************************************************
# ******************* DASK ***********************
# *****************************************************

def load_all_data_dask(market,signal=config["signal"],precision="D"):
    all_files = glob.glob(f"{config['dir']['data']}/{market}/{signal}/*/*")
    data = dd.read_parquet(all_files)
    data = convert_time_dask(data,rounding=precision)
    
    if signal=="trade":
        data = data.rename(columns={"trade-price":"price"})
    elif signal=="bbo":
        data["price"] = (data["bid-price"] + data["ask-price"])/2
    
    data = to_numeric_dask(data[["date","price"]])
    return data



# *****************************************************
# ******************* ALL DATES ***********************
# *****************************************************

def get_all_dates(signal=config["signal"],stock=config["stock"]):
    """return a sorted list of all dates were trades/bbo (signal) are available in the data"""
    def extract_date(s):
        try:
            date = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s).group(0)
        except:
            print(s)
        return date
    all_files = glob.glob(f"{config['dir']['data']}/*/{signal}/{stock}.[A-Z]*/*")
    all_dates = [extract_date(s) for s in all_files]
    all_dates = list(set(all_dates))
    all_dates.sort()
    return all_dates
