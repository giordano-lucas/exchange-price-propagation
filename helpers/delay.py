import pandas as pd


def generate_delayed_data(s1, s2, delay, join_type="outer"):
    s1 = s1.copy()
    s2 = s2.copy()
    s1.index = s1.index + pd.Timedelta(milliseconds=delay)
    pair_data = s1.join(s2, how=join_type, lsuffix="_1",
                        rsuffix="_2").ffill().dropna()
    return pair_data
