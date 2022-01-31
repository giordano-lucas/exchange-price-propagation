<img width="1195" alt="Screenshot 2022-01-29 at 09 13 05" src="https://user-images.githubusercontent.com/43466781/151653463-5805ec78-f73d-4237-939e-3bed2c09e147.png">
---
:point_right: Read our **data story** online [using the following link](https://giordano-lucas.github.io/exchange-price-propagation/) :rocket: 

# Abstract 

The financial world of equity trading relies on centralised exchanges. These exchanges are disseminated around the globe. Thus, it is sometimes possible to trade a share of one given company in multiple regions. Arbitrage pricing theory tells us that the price on those exchanges should roughly be equivalent. However, because information speed is bounded, shocks on a given share price might take some time to reach all exchanges and be incorporated into the new stock prices.

# Goal

This repository contains all the files used to analyze the price propagations delay for Shell's stock (RDSA) across multiple exchanges.

# Folders 
The repository contains the following folders : 

* `figures`: this folder contains HTML version of all the plotly figures produced during the analysis.
* `helpers`: contains multiple pythons scripts used to process, load and extract information from the raw data. It also contains the `config.yml` file.
* `results` : 
*  `scripts`

# Notebooks

* `data_exploration.ipynb`
* `lag_computer_dask.ipynb`
* `liquidity_computer.ipynb`
* `mean_price_and_ret_extractor.ipynb`
* `merge_all_dates_data.ipynb`
* `results_exploration.ipynb`
* `viz.ipynb`
* `viz_globe.ipynb`

# Files

# How to run the code
