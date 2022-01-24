from helpers import config
import glob
import re
import numpy as np
import pandas as pd
from .preprocessing import preprocessing_pipeline, convert_time
import traceback

def file_exist(path):
    return len(glob.glob(path)) > 0

# *****************************************************
# ******************** DAILY **************************
# *****************************************************

def __format_loaded_df(df, col, preprocessing_steps):
    df = df.rename(columns={col: "price"})
    series = df[["price", "date"]].drop_duplicates().set_index("date")
    series = preprocessing_pipeline(
            series,steps=preprocessing_steps )
    return series.replace([np.inf, -np.inf], np.nan).dropna()




def __load_bbo_file(file, preprocessing_steps):
    res = pd.read_csv(file, compression="gzip").rename(
        columns={"bid-price": "bid", "ask-price": "ask"})
    res = convert_time(res)
    res["mid"] = (res.bid + res.ask)/2
    return __format_loaded_df(res, "mid", preprocessing_steps)


def __load_trade_file(file, preprocessing_steps):
    res = pd.read_parquet(file)
    res = convert_time(res)
    res = res[res["trade-stringflag"] == "uncategorized"]
    return __format_loaded_df(res, "trade-price", preprocessing_steps)


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
        daily_data[market] = __load_trade_file(path, preprocessing_steps)
 
    return daily_data


# *****************************************************
# ******************* ALL DATES ***********************
# *****************************************************

def get_all_dates(stock='RDSA'):
    """return a sorted list of all dates were trades/bbo (signal) are available in the data"""
    def extract_date(s):
        try:
            date = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s).group(0)
        except:
            print(s)
        return date
    all_files = glob.glob(f"{config['dir']['data']}/*/trade/{stock}.[A-Z]*/*")
    all_dates = [extract_date(s) for s in all_files]
    all_dates = list(set(all_dates))
    all_dates.sort()
    return all_dates
