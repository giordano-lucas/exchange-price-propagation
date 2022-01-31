# Abstract
The financial world of equity trading relies on centralised exchanges. These exchanges are disseminated around the globe.
Thus, it is sometimes possible to trade a share of one given company in multiple regions. Arbitrage pricing theory tells us that the price on those exchanges should roughly be equivalent. However, because information speed is bounded, shocks on a given share price might take some time to reach all exchanges and be incorporated into the new stock prices.

# Motivation

This study aims to analyse how shocks propagate around exchanges located in different regions of the globe. The goal is to measure how fast price changes are flowing from one exchange to another. To do so, we propose to compute delayed correlations between the prices of the same stock across exchanges. 

Let's consider the `Microsoft (MSFT)` stock traded in `A` and `B` markets. The notation `MSFT.A` and `MSFT.B` will be used to refer to these time series. If we have $$i = 1,2,\ldots,n$$ observations for each time series, we can represent our sample using the following notation $$\{MSFT.A_{t+i}\}_{\forall i = 1,2,\ldots,n}$$ and similarly both `MSFT.B`. The `h` delayed or lagged time series of `MSFT.B` is therefore $$\{MSFT.B_{t+i+h}\}_{\forall i = 1,2,\ldots,n}$$. In short, the lagged times series is written as $$L_h(S_t)$$ so that $$L_0(S_t) = S_t$$. Note that `h` can take positive or negative values.

This concept is illustrated visually in the following figure: 

{% include_relative figures/plotly/motivation.html %}

Under the `x-axis`, you can find an interactive slider that allows shifting the time series of the stock traded in the XXX exchange (in'`blue`. By hovering the graph, you will be able to observe the `Pearson correlation` coefficient between the two time-series.

As expected, the general dynamics underlying the stochastic processes are almost equal. However, a better fit can be obtained by slightly shifting the XXX price by `- XXX ms`. It clearly indicates that there are indeed some differences in terms of information propagation and that delayed correlation are worth looking at.

> **Note**: this correlation estimator is ill-defined (as it will be explained later, the stationarity assumption between observation is not valid in this case). However this choice has been made to demonstrate the validity of the research question studied in this project. Indeed, the price times-series are easier to visualise and interpret than `log returns`.  

We expected to see a high correlation between these delays and the distances separating exchanges. For example, the delays between `NYSE` and `Euronext` should be higher than `NYSE` and `Nasdaq`. When analysing these delays over multiple years, we also expect the delays to:
1. Decrease over time due to the increase in hardware capabilities. More specifically, Moore's law tells us that the transmission speed of information doubles every year. Thus, the delays should, theoretically, decay exponentially over time.
2. Increase with the physical distance between the exchanges.


# Dataset

## Description

To conduct this study, we have access so almost `10 GB` of data. The latter contains high frequency daily data for both `trade` and `bbo` prices of the following stocks `Microsoft (MSFT)` and `Shell (RSDA)`. The first one was chosen because of its liquidity and market capitalisation in the `US` stock market when the second represents a stock that is traded both in `Europe (London and Amsterdam)` and the `USA`. Note that `Shell` is an actively traded company (XXX STATS XXX) and has been traded in Amsterdam and at NYSE since 2009, allowing us to have a lot of data across multiple years and distant regions. Hence, it can be used to model transatlantic information propagation across the period: 2005 to 2017.

In the code, the `MSFT` dataset is called `US sample`. `RDSa` files are aggregated under the name: `transatlantic dataset`. 

The following folder organisation is adopted:

    .
    ├── data                   # Data folder
    │ ├── markets              # directory containing all financial data
    │ │ ├── transatlantic      # GB, NL and US markets data for RDSa
    │ │ │ ├── GB
    │ │ │ │ ├── bbo
    │ │ │ │ │ ├── RDSa.L
    │ │ │ │ │ │ ├── ...        # example of file
    │ │ │ │ ├── trade          # trade transaction data
    │ │ │ │ │ ├── ...          # example of file
    │ │ ├── US_sample          # US markets data for MSFT
    │ ├── city                 # directory containing a city dataset with geographical coordinates
    │ │ ├── ...                # example of file
    │ ├── names                # directory containing the mapping ID -> name for the different exchanges
    │ │ ├── ...                # example of file
    └── ...                    # rest of files

## Preprocessing

The first step of our preprocessing journey is to filter out:

1. **Duplicated transactions**: sometimes they are duplicated rows in the dataset that can be removed to save some computations later on. Note that when two transactions have the time `xtime` but different prices, only the last (group order) will be kept. 
2. **Non-numeric prices**: we noticed that some prices actually contain symbols such as `(`, `)` or `#`. We cannot interpret them as numbers, so we chose to remove them from our dataset.

Usually, when it comes to multi-exchange intrady data, time zones are always worth looking at. However, in this case, we draw the attention of the reader to the fact that: for a stock price under $$GTM+x$$ time zone, we should have $$S_t \mid_{GTM+x}$$ $$ \approx S_t \mid_{GTM+y}, \; \forall_{x,y}$$ in order not to observe an arbitrage opportunity. This observation tells us that, we shouldn't normalise the time zones of our dataset. Conceptually, when an action (news, transaction, etc.) influencing the stock price occurs at time $$t$$ it should be incorporated simultaneously across all exchanges roughly at the same time $$t$$, irrespectively of the time zone. Actually, when two time-series are merged, only the overlapping time window shall be considered. 

As a last step, a log returns transformation is performed on the prices. Indeed, if we were to use the standard prices for the estimation of the correlation, we would implicitly assume long memory in the form of the mean of the process, which would introduce a bias for small lag values. In that regard, log-returns are more stationary process. This is one of the requirements of the [Hayashi-Yoshida correlation estimator introduced in the next section](#hayashi-yoshida-correlation-estimator).

Furthermore, multiple exchange data also imply multiple currencies. However, it is easy to show that Pearson correlations are invariant under linear transformations of input variables. In particular, if we assume a constant daily exchange rate, we don't need to convert the data into the same currency. 

Finally, for the `BBO` prices, we are only working with the mid price and only non-zero mid prices are considered.

> **Note**: for the reader’s information, we also considered different alternative preprocessing pipelines in our code such as binary returns (1, -1), moving averages or resampling methods. They are made available to the user inside the `helpers/preprocessing.py` file. However, we found that `log returns` simply outperformed the other techniques.


# Method 

To compare the two given signal $$S^1_t$$ and $$S^2_t$$ (same stock from exchange 1 and 2), we compute multiple correlations on lagged versions of the signals. Each used lag is then associated with a correlation measure as summarised in the following table.

| lag(ms)  | associated correlation              |
|----------|-------------------------------------|
|$$\cdots$$|  $$\cdots$$                         |
|  -1      |  $$corr(S^1_t$$,$$L_{-1}(S^2_t))$$  |
|  0       |  $$corr(S^1_t$$,$$L_{0}(S^2_t))$$   |
|  1       |  $$corr(S^1_t$$,$$L_{1}(S^2_t))$$   |
|  2       |  $$corr(S^1_t$$,$$L_{2}(S^2_t))$$   |
|$$\cdots$$|  $$\cdots$$                         |

> **Note**: in the following paragraphs, the terms `lag` and `delay` are used interchangeably and represents the same concept.

## Hayashi-Yoshida correlation estimator

Correlations are computed using the [Hayashi Yoshida](https://projecteuclid.org/download/pdf_1/euclid.bj/1116340299) covariance estimator for intraday time series observed only at discrete times in a non-synchronous manner.

Formally, is defined as follows:

$$C^{HY} = \sum_i^{n_1} \sum_j^{n_2} (S^1_{t_{1,i}} - S^1_{t_{1,i-1}}) \cdot (S^2_{t_{2,j}} - S^1_{t_{2,j-1}}) \cdot K_{i,j} = \sum_i^{n_1} \sum_j^{n_2} \Delta S^1_{t_1,i} \cdot \Delta S^2_{t_2,j} \cdot K_{i,j}$$

where $$K_{i,j} = I\{max(t_{1,i-1}, t_{2,j-1}) < min(t_{1,i}, t_{2,j})\}$$

An equivalent operation is to use returns $$R^1_t$$ and $$R^2_t$$ instead of the price changes.

The $$K_{i,j}$$ matrix imposes structure on how the join between both time series is computed. In practical applications, we may think of it as an `outer` join followed by the `forward fill` operation. On the joined time series, the `C^{HY}` estimator simply corresponds to a `Pearson` correlation.

Since we are using `Pearson` correlation under the hood, it is straightforward to associate `95%` confidence intervals to our estimations (see [article](https://faculty.washington.edu/gloftus/P317-318/Useful_Information/r_to_z/PearsonrCIs.pdf)). In all plots involving a correlation measure, we display confidence intervals that are interpreted as error bars. 
## Lag computation algorithm

Once we computed the lag associated with the highest correlation, it is extracted and saved. This operation is repeated for each day when the stock was traded and for every pair of exchanges available.  At this point, we obtain a daily time series of lags that can be interpreted as transmission delays of information flows across exchanges. 

Computations are done using the [Dask](https://dask.org/) framework. Dask allows for distributed computations of promise functions. All the dates to process are split into  `k` partitions. Each partition is then fed to a `Dask` process. The process iterates over the dates of the given partition and every time a date is processed it writes the results in a dedicated file (one file is produced per partition). By doing so, it is possible to stop the computation and restart it later, the task function does process date for which there already exists results in the file. It takes around 1h to process the `trade` data and 1h30 to process `bbo` data. These computations were done on our personal computer having the following characteristics :

| Hardware type  | configuration       |
|----------------|---------------------|
|  CPU           |i7-7700 HQ 8 cores   |
|  RAM           |  16 GO               |

To compute optimal lag for one given date, we need to run a peak finding optimisation algorithm.

## Peak finding algorithm: a grid search approach

To find the lag corresponding to the maximum correlation value, we follow a grid search approach. In other words, we:

1. Select a range of possible lag values.
1. Compute the correlation for each of them.
1. Report the `argmax` of the correlation array.

However, this approach raises multiple challenges: one has to choose a `step_size` for the lags range as well as an exploration `window` to iterate over (e.g. $$[-20 \; ms, +350 \; ms]$$).  These choices have an important impact on the computation time and the obtained performances: choosing a wide `window` and a small `step_size` will always ensure that the true peak is captured. However, this setting yields a high computation time since we can possibly explore irrelevant regions of the parameter space. 

To speed up this process, we developed a greedy algorithm that dynamically updates the `step_size` and `window` parameters. We start with a guess and iterate until convergence. It follows the following set of requirements:

1. If the lagged correlation function appears to be increasing in one direction, the algorithm increases the `step_size` (`+50%`) and moves the `window` toward that direction.
1. In the other case (not strictly increasing), the algorithm centres the `window ` to the current identified peak (there must be such a peak otherwise the function is increasing) and reduces  the `step_size` (`-50%`). 

This algorithm is better illustrated in the following example. 

At iteration `0`, the lagged correlations are computed using the default `step_size`:

{% include_relative figures/peak_algo/Correlation_vs_delay_window_iteration_0_market_NL_US.html %}

We see on the previous plot that the maximum peak is not centred. At iteration `1`, the `window` is centred and the XXX

{% include_relative figures/peak_algo/Correlation_vs_delay_window_iteration_1_market_NL_US.html %}

{% include_relative figures/peak_algo/Correlation_vs_delay_window_iteration_2_market_NL_US.html %}

{% include_relative figures/peak_algo/Correlation_vs_delay_window_iteration_3_market_NL_US.html %}

TODO: Augustin

TODO: Bechmarks 

TODO: Intro to Dask


# Data exploration

## Descriptive statistics

In this section, statistics on the `transatlantic` dataset are provided. In particular, the number of transactions for the different exchanges is computed below:

{% include_relative figures/plotly/nb_transaction_per_exchange.html %}

As expected, we observe more data points for the `bbo` dataset. Another interesting fact is that the `Amsterdam market` contains more transactions that the `London market` even though the latter is the primary exchange for `Shell`. 

Secondly, the size of the joined time series is shown below. It allows us to assess the quality of the error bars displayed in the cross-correlation plots. For instance, if the join size is `100`, we won't be able to get meaningful estimates for the correlation.

{% include_relative figures/plotly/nb_transaction_join_market_pairs.html %}

XXXX

Finally, several classical financial statistics are shown in the table below:

| Statistic                                               | value             |
|---------------------------------------------------------|-------------------|
|the mean duration between two consecutive trades         |    6.3s           |
|average number of trades per day                         |  2800 trades      |
|the average tick size δ in percentage of the midquote    |                   |
|the average bid/ask spread expressed in tick size        |                   |
|the frequency of unit bid/ask spread                     |                   |


We also give a few information regarding the exchanges considered in this study.

| ID    | Name                     | Country        | Trading hours (CET) |   Currency      |
|-------|--------------------------|----------------|---------------------|-----------------|
| `.L`  | Amsterdam Stock Exchange | Netherlands    | 09:00-17:30         | EUR             |
| `.AS` | London Stock Exchange    | United Kingdom | 09:00-17:30         | GBP             |
| `.N`  | New York Stock Exchange  | USA            | 09:00-17:30         | USD             |

## Visual validation of the method

As a first validation steps, we propose to compute the autocorrelation of the `MSFT` stock on the `US` market. From the stylised facts of financial returns, we know that we should observe any serial autocorrelation. Therefore, we would expect to see a `Dirac` function for this plot with a correlation of `1` at lag `0`.

{%  include_relative figures/peak_algo/Correlation_vs_delay_window_iteration_0_market_NL_US.html %}

We indeed observe a `Dirac` behaviour for this plot which confirms our beliefs. A slightly more interesting case is the comparison `US - GB` markets of the following plot.

{%  include_relative figures/peak_algo/Correlation_vs_delay_window_iteration_0_market_NL_US.html %}

Again, a correlation peak occurs at `lag = 0 ms`. However, the magnitude of the peak is lower than the one of the previous plot. Furthermore, we observe higher variability for other lags than `0` compared to the previous plot.
 
The shape of these plots are similar to those of the [High Frequency Lead/lag Relationships](https://arxiv.org/ftp/arxiv/papers/1111/1111.7103.pdf) paper. Furthermore, we observe strongly asymmetrical cross-correlation functions. However, interestingly, the maximum correlation reachable is lower than those in the paper. Indeed, the second plot shows a correlation on only `30%`. Given the fact that we are dealing with the same stock price (only in different exchanges), we would have expected a higher correlation. We found that it this behaviour is strongly impacted by the difference in frequencies between the two exchanges. If one is particularly liquid compared to the other, the `forward fill` operation will, roughly speaking, transform our low-frequency signal to a strong piece-wise step function. In opposition, the high frequency log return signal will juggle around the constant threshold defined by the low-frequency signal. As a result, it creates artefacts that reduce the overall correlation. Hence, it is not surprising to observe a maxmium correlation in the order of `5%` for some liquid-illiquid pairs.

Moreover, it is important to notice that the shape of the plots is largely dependent on the scale of the `x-axis` (e.g. `10 ms`, `10 s` or `100 s`). The larger the scale, the straighter the peak of `Dirac` function. This is relevant to interpret the plots show below and also to be able to compare our results with those of the [High Frequency Lead/lag Relationships](https://arxiv.org/ftp/arxiv/papers/1111/1111.7103.pdf) paper, i.e. the authors mostly focus on larger time scales (e.g. figure 1 is in trading days).

Finally, it is important to notice that the error bars are usually quite large and multiple overlaps occur. Therefore,  except for the peak at `0` there is no statistical evidence that the correlation estimates are different. 

> **Note**: to keep our optimisation algorithm simple and fast, we do not consider error bars. As a result, the maximum lag estimation is not as robust as it could be.
