<img width="1195" alt="Screenshot 2022-01-29 at 09 13 05" src="https://user-images.githubusercontent.com/43466781/151653463-5805ec78-f73d-4237-939e-3bed2c09e147.png">
---

:point_right: Read our **data story** online [using the following link](https://giordano-lucas.github.io/exchange-price-propagation/) :rocket: 

# Abstract 

The financial world of equity trading relies on centralised exchanges. These exchanges are disseminated around the globe. Thus, it is sometimes possible to trade a share of one given company in multiple regions. Arbitrage pricing theory tells us that the price on those exchanges should roughly be equivalent. However, because information speed is bounded, shocks on a given share price might take some time to reach all exchanges and be incorporated into the new stock prices.

# This repository

This repository contains all the files used to analyze the price propagations delay for Shell's stock (RDSA) across multiple exchanges. It is organized into multiple folders and notebooks.

# Folders 
The repository contains the following folders : 

* `figures`: this folder contains HTML version of all the plotly figures produced during the analysis.
* `helpers`: contains multiple pythons scripts used to process, load and extract information from the raw data. It also contains the `config.yml` file. More details about these files [here](https://github.com/giordano-lucas/exchange-price-propagation/tree/main/helpers).
* `results` : folder containing results of big computations such as the `lags` time series.
* `scripts` : contains a script used to efficiently push figures on the desired GitHub branch.


# Notebooks
Most of the analysis is performed through notebooks. They all used the helper function defined in [./helper](https://github.com/giordano-lucas/exchange-price-propagation/tree/main/helpers) and are organized as follows :

* `data_exploration.ipynb` : first glance at the raw data. It contains the experiments that we conducted on the data to understand how to approach the problem. We also developed the `peak_finding`  algorithm in that notebook.
* `lag_computer_dask.ipynb` : combines the  `peak_finding` algorithm with [dask helpers](https://github.com/giordano-lucas/exchange-price-propagation/blob/main/helpers/dask.py) to compute and save (into the `results` folder) the daily lags. 
* `liquidity_computer.ipynb` : compute the `liquidity` metric (daily median of the period between two consecutive trades) using dask.
* `mean_price_and_ret_extractor.ipynb` : extracts (using dask) the daily mean price and returns from the data files (one file per day) into time series. 
* `results_exploration.ipynb` : in this notebook, we study the obtained results (`lags`) and generate multiple plots out of them. These plots are saved in the `figures` folder.
* `viz.ipynb` : contains interative visulaization of the data.  
* `viz_globe.ipynb` : contains a visual comparison of the `lags` with the distance separating exchanges using a world globe.
* `simple_stats.ipynb` : contains some simple statistics (average number of trades per day...)

# Files
* `runtime.txt` :  file created by Heroku. Do not modify it.
* `requirements.txt` : text file containing the requirements to run the code. 
# How to run the code
To run the analysis by yourself follow the described steps : 
1. run the command `pip install -r requirements.txt
` to obtain the needed libraries to run the code.
2. edit the `helpers/config.yml` file to chose the signal to work with :  `trade` of `bbo`.
3. Download the data into a folder named `data`. Information about how to organize the data can be found in the `helpers/config.yml` file.
4. Run the "computational" notebooks : `lag_computer_dask.ipynb`, `liquidity_computer.ipynb` and `mean_price_and_ret_extractor.ipynb`.
5. Run the analysis and visualization notebooks : `data_exploration.ipynb`, `results_exploration.ipynb`,`viz.ipynb`,`simple_stats.ipynb` and `viz_globe.ipynb`.
