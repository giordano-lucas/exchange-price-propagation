import pandas as pd
from helpers.stats import compute_correlation


def generate_delayed_data(s1, s2, delay, join_type="outer"):
    s1 = s1.copy()
    s2 = s2.copy()
    
    h = min(s1.index.max(),s2.index.max())
    l = max(s1.index.min(),s2.index.min())
    
    s1.index = s1.index + pd.Timedelta(milliseconds=delay)
    pair_data = s1.join(s2, how=join_type, lsuffix="_1",
                        rsuffix="_2").ffill().dropna()
    return pair_data[(l<=pair_data.index)*(pair_data.index<=h)]


def compute_delays(df, n1, n2, center=0, step_size=1000, n_step=20):
    correlations = []
    los = []
    his = []

    delays = range(center-n_step*step_size, center+n_step*step_size, step_size)
    for delay in delays:
        s1, s2 = df[n1].copy(), df[n2].copy()
        pair_data = generate_delayed_data(s1, s2, delay)
        if len(pair_data)==0:
            corr, lo, hi = 0,0,0
        else :    
            corr, lo, hi = compute_correlation(pair_data)
        correlations.append(corr)
        los.append(corr-lo)
        his.append(hi-corr)
    return delays, correlations, los, his, 
