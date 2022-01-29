# Abstract
The financial world of equity trading relies on centralized exchanges. These exchanges are disseminated around the globe.
Thus, it is sometimes possible to trade a share of one given company in multiple regions. Abitrage pricing theory tells us that the price on those exchanges should roughly be equivalent. However, bcause information speed is bounded, shocks on a given share price might take some time to reach all exchanges and be incorporated into the new stock prices.

# Motivation

This study aims to analyse how shocks propagate around exchanges located in different regions of the globe. The goal is to measure how fast price changes are flowing from one exchange to another. To do so, we propose to compute delayed correlations between the prices of the same stock accross exchanges. 

Let's consider the `Microsoft (MSFT)` stock traded in `A` and `B` markets. The notation `MSFT.A` and `MSFT.B` will be used to refer to these time series. If we have $$i = 1,2,\ldots,n$$ observations for each time series, we can represent our sample using the following notation $$\{MSFT.A_{t+i}\}_{\forall i = 1,2,\ldots,n}$$ and similarly both `MSFT.B`. The `h` delayed or lagged time series of `MSFT.B` is therefore $$\{MSFT.B_{t+i+h}\}_{\forall i = 1,2,\ldots,n}$$. In short, the lagged times series is written as $L_h(S_t)$$ so that $$L_0(S_t) = S_t$$. Note that `h` can take postive or negative values.

This concept is illustrated visually in the following figure: 

{% include_relative figures/plotly/motivation.html %}

Under the `x-axis`, you can find a interactive slider that allows to shift the time series of the stock traded in the XXX exchange (in'`blue`. By hovering the graph, you will be able to observe the `Pearson correlation` coeficient between the two time series.

As expected, the general dynamics underlying the stochastic processes are almost equal. However, a better fit can be obtained by slighly shifting the XXX price by `- XXX ms`. It clrealy indicates that there are indeed some differences in terms of information propagation and that delayed correlation are worth looking at.

> **Note**: this correaltion estimator is ill-definied (as it will be explained later, the stationnarity assupmtion between observation is not valid in this case). However this choice has been made to demonstrate the validity of the research question studied in this project. Indeed, the price times series are easier to visualize and interpret than `log returns`.  

We expected to see a high correlation between these delays and the distances separating exchanges. For example, the delays between `NYSE` and `Euronext` should be higher than `NYSE` and `Nasdaq`. When analyzing these delays over multiple years we also expect the delays to:
1. Decrease over time due to the increase in hardware capabilities. More specifically, Moore's law tells us that the transmission speed of information doubles every year. Thus, the delays should, theoratically, decay exponentially over time.
2. Increase with the physical distance between the exchanges.

# Dataset

## Description

To conduct this study, we have acess so almost `10 GB` of data. The latter contains high frequency daily data for both `trade` and `bbo` prices of the following stocks `Microsoft (MSFT)` and `Shell (RSDA)`. The first one was chosen because of its liquidity and market capitilasation in the `US` stock market when the second represents a stock that is traded both in `europe (London and Amesterdam)` and the `USA`. Note that `Shell` is an actively traded company (XXX STATS XXX) and has been traded in Amsterdam and at NYSE since 2009, allowing us to have a lot of data across multiple years and distant regions. Hence, it can be used to model transatlantic information propagation across the period: 2005 to 2017.

In the code, the `MSFT` dataset is called `US sample`. `RDSa` files are aggregated under the name : `transatlantic dataset`. 

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

1. **Duplicated transactions**. Note that when two transactions have the time `xtime` but different prices, only the last (group order) will be kept. 
2. **Non numeric prices**: we noticed that some prices actually contain symbols such as `(`, `)` or `#`. We can not interperet them as numbers, so we chose to remove them from our dataset.

Usually, when it comes to multi-exchanges intrady data, time-zones are always . However, in this case, we draw the attention of the reader to the fact that: for a stock price under $$GTM+x$$ time zone, we should have $$S_t \mid GTM+x$$ $$ \approx S_t \mid GTM+y, \; \forall_{x,y}$$ in order not to observe an arbtrage opportunity. This observation tells us that, we shouldn't normalise the time zones of our dataset. Conceptually, when a action (news, transaction, etc.) influencing the stock price occurs at time $$t$$ it should be incorporated simultaneously accross all exchanges roughly at the time $$t$$, irrespectively of the time zone. Actually, when two time time series are merged, only the overlapping time window shall be considered. 

As a last step, a log returns transformation is performed on the prices. Indeed, if we were to use the standard prices for the estimation of the correlation, we would implicity assume long memory in the form of the mean of the process, which would introduce a bias for small lag values. In that regard, log-returns are more stationary process. This is one of the requirements of the [Hayashi-Yoshida correlation estimator introduced in the next section](#hayashi-yoshida-correlation-estimator).

Furthemore, multiple exchange data also imply multiple currencies. However, it is easy to show that pearson correlations are invariant under linear transformations of input varibles. In particular, if we assume a constant daily echange rate, we don't need to convert the data into the same currency. 

Finally, for the `BBO` prices, we are only working with the mid price and only non-zero mid prices are considered.

> **Note**: for the readers information, we also considered different alternative preprocessing pipelines in our code such as binary returns (1, -1), moving averages or resampling methods. They are made available to the user inside the `helpers/preprocessing.py` file.

# Method 

To compare two given signals $$S^1_t$$/$$S^2_t$$ (same stock from exchange 1 and 2), we compute multiple correlations on lagged versions of the signals. Each used lag is then associated with a correlation as follows :

| lag(ms)  | associated correlation              |
|----------|-------------------------------------|
|$$\cdots$$|  $$\cdots$$                         |
|  -1      |  corr($$S^1_t$$,$$L_{-1}(S^2_t)$$   |
|  0       |  corr($$S^1_t$$,$$L_{0}(S^2_t)$$)   |
|  1       |  corr($$S^1_t$$,$$L_{1}(S^2_t)$$)   |
|  2       |  corr($$S^1_t$$,$$L_{2}(S^2_t)$$)   |
|$$\cdots$$|  $$\cdots$$                         |

## Hayashi-Yoshida correlation estimator

Correlations are computed using the [Hayashi Yoshida](https://projecteuclid.org/download/pdf_1/euclid.bj/1116340299) intraday estimator for time series observed only at discrete times in a non-synchronous manner

Formally, it is defined as follows:

$$C^{HY} = \sum_i^{n_1} \sum_j^{n_2} (S^1_{t_{1,i}} - S^1_{t_{1,i-1}}) \cdot (S^2_{t_{2,j}} - S^1_{t_{2,j-1}}) \cdot K_{i,j} = \sum_i^{n_1} \sum_j^{n_2} \Delta S^1_{t_1,i} \cdot \Delta S^2_{t_2,j} \cdot K_{i,j}$$

where $$K_{i,j} = I\{max(t_{1,i-1}, t_{2,j-1}) < min(t_{1,i}, t_{2,j})\}$$

An equivalent operation is to use returns $$R^1_t$$ and $$R^2_t$$ instead of the price changes.

The $$K_{i,j}$$ matrix imposes structure on how the join between both time series is computed. In practical applications, we may think of it as an `outer` join followed by the `formward fill` operation.  
## Optimisation algorithm

Once we computed the lag associated with the highest correlation is extracted and saved. This operation is repeated every day the stock was traded and for every pair of exchanges available. 
At this point, we obtain a time series of lags (one per day) that are interpreted as transmission delays. 
[ss](#method)

TODO: Augustin

TODO: Bechmarks 

TODO: Intro to Dask

# Data exploration

## Descriptive statistics

In this section, statistics on the `transactlantic` dataset are provided. In particular, the number of transactions for the different exchanges is computed below:

{% include_relative figures/plotly/nb_transaction_per_exchange.html %}

As expected, we observe more data points for the `bbo` dataset. Another interesting fact is that the `Amsterdam market` contains more transactions that the `London market` even though the latter is the primary exchange for `Shell`. 

Secondly, the size of the joined time series is shown below. It allows us to assess the quality of the error bars displayed in the cross-correlation plots. For instance, if the join size is `100`, we won't be able to get meaningfull estimates for the correlation.

{% include_relative figures/plotly/nb_transaction_join_market_pairs.html %}

XXXX

Finally, several classical financial statistics are shown in the table below:

| Statistic                                               | vaue              |
|---------------------------------------------------------|-------------------|
|the median duration between two consecutive trades       |                   |
|the average tick size δ in percentage of the midquote    |                   |
|the average bid/ask spread expressed in tick size        |                   |
|the frequency of unit bid/ask spread                     |                   |


We also give a few information regarding the exchanges considered in this study

| ID    | Name                     | Country        | Trading hours (CET) |   Currency      |
|-------|--------------------------|----------------|---------------------|-----------------|
| `.L`  | Amsterdam Stock Exchange | Netherlands    | 09:00-17:30         | EUR             |
| `.AS` | London Stock Exchange    | United Kingdom | 09:00-17:30         | GBP             |
| `.N`  | New York Stock Exchange  | USA            | 09:00-17:30         | USD             |

## Visual validation of the method

As a first validation steps, we propose to compute the auto-correlation of the `MSFT` stock on the `US` market. From the stylised facts of financial returs, we know that we should observe any serial autocorrelation. Therefore, we would expect to see a `Dirac` function for this plot with a correlation of `1` at lag `0`.

{% include_relative figures/plotly/Correlation_vs_lag_iteration(0)_market(US_US).html %}

We indeed observe a `Dirac` behaviour for this plot which confirms our believes. A slighly more intersting case is the comparision `US - GB` markets of the following plot

{% include_relative figures/plotly/Correlation_vs_lag_iteration(0)_market(US_GB).html %}

Again, a correlation peak occurs at `lag = 0 ms`. However, the magnitude of the peak is lower than the one of the previous plot.
 
The shape of these plots are similar to those of the XXX paper. Furthermore, we observe strongly assymetrical cross-correlation functions. However, interestingly, the maximum correlation reachable is lower that those in the paper. Indeed, the second plot shows a correlation on only `30%`. Given the fact that we are dealing with the same stock price (only in different exchanges), we would have expected a higher correlation. We found that it this behaviour is strongly impacted by the difference in frequencies between the two exchanges. If one is particuarly liquid compared to the other, the `forward fill` operation will, roughly speaking, transform our low frequency signal to a strong piece-wise step function. In opposition, the high frequnecy log return signal will jaggle around the contant threshold defined by the low frequnecy signal. As a result, it creates artificats that reduce the overall correlation. Hence, it is not surprising to observe a maxmium correlation in the order of `5%` for some liquid-illiquid pairs.

Moreover, it is important to notice that the the shape of the plots is largely dependant on the scale of the `x-axis` (e.g. `10 ms`, `10 s` or `100 s`). The larger the scale, the straigher the peak of `Dirac` function. This is relevant to interpret the plots show below and also to be able to compare our results with those of the XXX paper, i.e the authors mostly focus on larger time scales (e.g figure 1 is in trading days).

# Analysis

## Time plot

TODO: Augustin

## Distance plot 

TODO: Augustin
## More visualisations 

### Customisable historical lag
To conclude our projet, we made available additional interactive visualisations of the computed lags.

The first one is an extended version of the plot shown in [section ***Time Plot***](#time-plot). It handles the following user actions: 

- Select the input data: `bbo` or `trade` prices.
- Select the averaging window.
- Change the sampling frequency of the signal (daily, weekly, monthly).
- Zoom in/out in a particular window of the `x-axis`.

The visualation is available [at this address](https://murmuring-garden-88123.herokuapp.com/)

> **Note**: this application runs in a free container within the ***Heroku*** platform. Hence, it may take a couple of seconds to load.

We could not embed this plot in this website because `GitHub pages` only supports static websites. The resampling and moving averages operations required a dynamic server and we have to use ***Heroku*** in that regard.
### Propagation speed vs distances on the globe

This last plot aims to provide yet another way of visualising the progation speed. In this form, because only 3 data points are available, the plot is not very usefull. Nevertheless, the code is already setup and could be fed with additional data points at a later stage. We thought this plot has a clear potential and that it would be interesting to start the developpment.

> **Note**: this plot was constructed using the `GeoPandas` library.

# Further steps

We observed substancial variability in the distribution of lags. This is mainly related to the fact that:
1. the analysis was only conducted for the `RSDA` stock. 
2. The greedy optimisation algorithm sometimes produces outliers

Averaging the results across multiple stocks shall help reducing the variance of the estimation. 

Finally, one of the intial objectives was to try to reconstruct Moore's from the dataset.



# Conclusion 

TODO: Augustin ou Lucas

Through this project, we 
