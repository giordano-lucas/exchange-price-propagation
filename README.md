# Big Data For Finance Project
---

# Data Specification 

1. Focus on trade price
2. How to join :
    - Type : full outer join ? Merge with nearest key ([pd.merge_asof](https://pandas.pydata.org/pandas-docs/dev/reference/api/pandas.merge_asof.html)) ? 
    - On only shared market hours ? It creates large discontinuities when we concatenate all daily files. Furthemore, not sure it's the right way to go when we deal with shifted correlation  (solution would be to use the shared market hours after shift).
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

## Other metric

We though about computing the lagged difference in terms of price and  compute 

 >  `arg max MSE(stock(t), stock(t-tau)`

# Visualization

1. Interactive visualisation of `C` 
2. Optimum delay visualisation 

# Analysis

Construct stylised facts on the metric (correclation, MSE of lagged difference) and see if they behave like log-returns and if there is some predictibility 
# Report

Data Story style
