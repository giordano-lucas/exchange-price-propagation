from helpers import config
import glob
import re
import numpy as np
import pandas as pd
from .preprocessing import convert_time, transform_to_returns


def file_exist(path):
    return len(glob.glob(path)) > 0


def __format_loaded_df(df, col, to_returns):
    df = df.rename(columns={col: "price"})
    df = df[["price", "date"]].drop_duplicates().set_index("date")
    if to_returns:
        df = transform_to_returns(df)
    return df


def __load_bbo_file(file, to_returns=True):
    res = pd.read_csv(file, compression="gzip").rename(
        columns={"bid-price": "bid", "ask-price": "ask"})
    res = convert_time(res)
    res["mid"] = (res.bid + res.ask)/2
    return __format_loaded_df(res, "mid", to_returns)


def __load_trade_file(file, to_returns=True):
    res = pd.read_parquet(file)
    res = convert_time(res)
    res = res[res["trade-stringflag"] == "uncategorized"]
    return __format_loaded_df(res, "trade-price", to_returns)

def load_daily_data(date,stock,locations = config['location'], to_returns=False):
    daily_data = {}
    signal = config["signal"]
    for location in locations :
        mkt_suffix = config["markets"]["suffix"][location]
        path_expr = f"data/markets/{location}/{signal}/{stock}{mkt_suffix}/{date}*.parquet"        
        print(path_expr)
        path = glob.glob(path_expr)[0]
        daily_data[location] = __load_trade_file(path, to_returns)
     
    return daily_data
