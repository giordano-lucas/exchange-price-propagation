This folder of the directory contains scripts and files used by the notebooks to conduct the analysis. 

# Python files
* `algorithm.py`  : peak finding algorithm
* `dask.py`  : helper functions to use dask. For example, it contains functions to save results from a partitioned task work into multiple files and merge them afterwards.
* `delay.py` : functions to compute lags/delays across 2 exchanges over a given range of lags.
* `loading.py`: loading functions that load and preprocess the raw data into dask/pandas dataframes.
* `plots.py` : contains a single function that helps saving (into the `Figures` folder) generated plots as HTML files.
* `preprocessing.py` : contains all preprocessing functions needed to apply to the data and results (reformat the dates, compute log-returns...)
* `stats.py` : functions helping to compute correlations and their confidence intervals. The formulas used in that file come from [Pearson Correlation CI in Python](https://zhiyzuo.github.io/Pearson-Correlation-CI-in-Python/)

# Other files
* `config.yml` : The config file contains all information needed to run the code. It contains the paths to all data and result files. One can set here the signal (`bbo` or `trade`) to work with. It also contains a list of the available markets.
