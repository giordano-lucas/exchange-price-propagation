# Abstract
The financial world of equity trading relies on centralized exchanges. These exchanges are disseminated around the globe.
Thus, it is sometimes possible to trade a share of one given company in multiple regions. Abitrage pricing theory tells us that the price on those exchanges should roughly be equivalent. However, bcause information speed is bounded, shocks on a given share price might take some time to reach all exchanges and be incorporated into the new stock prices.

# Motivation

This study aims to analyse how shocks propagate around exchanges located in different regions of the globe. The goal is to measure how fast price changes are flowing from one exchange to another. To do so, we propose to compute delayed correlations between the prices of the same stock accross exchanges. 

Let's consider the `Microsoft (MSFT)` stock traded in `A` and `B` markets. The notation `MSFT.A` and `MSFT.B` will be used to refer to these time series. If we have $$i = 1,2,\ldots,n$$ observations for each time series, we can represent our sample using the following notation $$\{MSFT.A_{t+i}\}_{\forall i = 1,2,\ldots,n}$$ and similarly both `MSFT.B`. The `h` delayed or lagged time series of `MSFT.B` is therefore $$\{MSFT.B_{t+i+h}\}_{\forall i = 1,2,\ldots,n}$$. In short, the lagged times series is written as $$L_h(S_t)$$ so that $$L_0(S_t) = S_t$$. Note that `h` can take postive or negative values.

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
|  -1      |  $$corr(S^1_t$$,$$L_{-1}(S^2_t))$$  |
|  0       |  $$corr(S^1_t$$,$$L_{0}(S^2_t))$$   |
|  1       |  $$corr(S^1_t$$,$$L_{1}(S^2_t))$$   |
|  2       |  $$corr(S^1_t$$,$$L_{2}(S^2_t))$$   |
|$$\cdots$$|  $$\cdots$$                         |

