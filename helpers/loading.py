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

class Loader:
    def __init__(self, preprocessing_steps=['numeric', 'log_returns'], dataset='transatlantic') -> None:
        self.preprocessing_steps = preprocessing_steps
        self.dataset = dataset
        
    def load_daily_data(self, date):
        daily_data = {}
        for market in config[self.dataset]['markets']['list']:
            mkt_suffix = config[self.dataset]['markets']['suffix'][market]
            path_expr = f"{config['dir']['data']}/{self.dataset}/{market}/{config[self.dataset]['signal']}/{config[self.dataset]['stock']}.{mkt_suffix}/{date}-*.{config[self.dataset]['extension']}*"
            path = glob.glob(path_expr)
            if len(path) == 0:
                print(f"missing data : market {market} for {date} ")
                continue
            else:
                path = path[0]
                daily_data[market] = self.__get_load_file()(path)

        return daily_data

    ##########################################
    ########### Private helper ft ############
    ##########################################


    def __format_loaded_df(self, df, col):
        df = df.rename(columns={col: "price"})
        series = df[["price", "date"]].drop_duplicates().set_index("date")
        series = series[~series.index.duplicated(keep='first')]
        series = preprocessing_pipeline(
                series,steps=self.preprocessing_steps)
        series = series.replace([np.inf, -np.inf], np.nan).dropna()
        series = series[np.abs(series.price) > 0.0]
        return series

    def __load_bbo_file(self, file):
        res = self.__get_read_file(file).rename(
            columns={"bid-price": "bid", "ask-price": "ask"})
        res = convert_time(res)
        res["mid"] = (res.bid + res.ask)/2
        return self.__format_loaded_df(res, "mid")

    def __load_trade_file(self, file):
        res = self.__get_read_file(file)
        res = convert_time(res)
        res = res[res["trade-stringflag"] == "uncategorized"]
        return self.__format_loaded_df(res, "trade-price")

    def __get_load_file(self):
        if config[self.dataset]['signal'] == 'trade':
            return self.__load_trade_file
        else:
            return self.__load_bbo_file
    
    def __get_read_file(self, file):
        if config[self.dataset]['extension'] == 'csv':
            return pd.read_csv(file, compression='gzip')
        else:
            return pd.read_parquet(file)


# *****************************************************
# ******************* ALL DATES ***********************
# *****************************************************

def get_all_dates(signal,stock='RDSA'):
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
