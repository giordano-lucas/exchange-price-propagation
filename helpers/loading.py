from helpers import config
import glob
import re
import numpy as np
import pandas as pd
from .preprocessing import convert_time, transform_to_returns

import dask
dask.config.set(scheduler="processes")


def __load_bbo_file(file):
    res = pd.read_csv(file, compression="gzip").rename(
        columns={"bid-price": "bid"})
    res = convert_time(res)
    res = res[res.bid > 0]
    #res = res.bid.diff(1).dropna()>0
    return res[["bid", "xltime"]].drop_duplicates().set_index("xltime")


def __load_trade_file(file, to_returns):
    res = pd.read_csv(file, compression="gzip")
    res = convert_time(res)
    res = res[res["trade-stringflag"] == "uncategorized"]
    res = res[["trade-price", "date"]].drop_duplicates().set_index("date")
    if to_returns:
        res = transform_to_returns(res)
    return res


def load_daily_data(date, to_returns=False):
    daily_data = {}
    for market in config['markets']:
        path_expr = f"./{config['dir']['data']}/{config['signal']}/{config['stock']}.{market}/{date}*.csv.gz"
        try:
            path = glob.glob(path_expr)[0]
            daily_data[market] = __load_trade_file(path, to_returns)
        except:
            print(f"missing data : {date} {market}")
    return daily_data
