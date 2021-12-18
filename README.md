# Big Data For Finance Project
---

# Data Specification 

1. Focus on trade price
2. Full outer join ? Merge with nearest key ([pd.merge_asof](https://pandas.pydata.org/pandas-docs/dev/reference/api/pandas.merge_asof.html)) ? 
3. Loaded with `Dask` ?
# Correlation

## Description
1. Build correlation `C` 3D tensor (with confidence intervals):
    -  1st axis : Exchange 1
    -  2nd axis : Exchange 2
    -  3rd axis : Correlation delay (bounded e.g. 10 seconds)
2. Compute optimum delay for each exchange pair (accross various time steps). 

## Questions 

1. Need for noise reduction ?
2. Need for different  correlation measures (pearson, rank, etc.) ?
3. Rolling computation ?

# Visualization

1. Interactive visualisation of `C` 
2. Optimum delay visualisation 

# Report

Data Story style
