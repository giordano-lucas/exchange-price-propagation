import numpy as np
from scipy import stats


def compute_correlation(pair_data, CI=True):
    s1, s2 = pair_data["price_1"].values, pair_data["price_2"].values
    N = len(s1)
    corr, p_val = stats.pearsonr(s1, s2)
    if not CI:
        return corr
    else:
        lo, hi = __compute_ci(corr, p_val, N)
        return corr, lo, hi

# from https://zhiyzuo.github.io/Pearson-Correlation-CI-in-Python/


def __compute_ci(corr, p_val, N):
    r_z = np.arctanh(corr)
    se = 1/np.sqrt(N-3)
    alpha = 0.05
    z = stats.norm.ppf(1-alpha/2)
    lo_z, hi_z = r_z-z*se, r_z+z*se
    lo, hi = np.tanh((lo_z, hi_z))
    return lo, hi
