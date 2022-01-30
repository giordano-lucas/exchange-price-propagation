# Abstract
The financial world of equity trading relies on centralized exchanges. These exchanges are disseminated around the globe.
Thus, it is sometimes possible to trade a share of one given company in multiple regions. Abitrage pricing theory tells us that the price on those exchanges should roughly be equivalent. However, bcause information speed is bounded, shocks on a given share price might take some time to reach all exchanges and be incorporated into the new stock prices.

# Motivation

This study aims to analyse how shocks propagate around exchanges located in different regions of the globe. The goal is to measure how fast price changes are flowing from one exchange to another. To do so, we propose to compute delayed correlations between the prices of the same stock accross exchanges. 

Let's consider the `Microsoft (MSFT)` stock traded in `A` and `B` markets. The notation `MSFT.A` and `MSFT.B` will be used to refer to these time series. If we have $$i = 1,2,\ldots,n$$ observations for each time series, we can represent our sample using the following notation $$\{MSFT.A_{t+i}\}_{\forall i = 1,2,\ldots,n}$$ and similarly both `MSFT.B`. The `h` delayed or lagged time series of `MSFT.B` is therefore $$\{MSFT.B_{t+i+h}\}_{\forall i = 1,2,\ldots,n}$$. In short, the lagged times series is written as $L_h(S_t)$$ so that $$L_0(S_t) = S_t$$. Note that `h` can take postive or negative values.

This concept is illustrated visually in the following figure: 

% include_relative figures/plotly/motivation.html %

Under the `x-axis`, you can find a interactive slider that allows to shift the time series of the stock traded in the XXX exchange (in'`blue`. By hovering the graph, you will be able to observe the `Pearson correlation` coeficient between the two time series.

As expected, the general dynamics underlying the stochastic processes are almost equal. However, a better fit can be obtained by slighly shifting the XXX price by `- XXX ms`. It clrealy indicates that there are indeed some differences in terms of information propagation and that delayed correlation are worth looking at.

> **Note**: this correaltion estimator is ill-definied (as it will be explained later, the stationnarity assupmtion between observation is not valid in this case). However this choice has been made to demonstrate the validity of the research question studied in this project. Indeed, the price times series are easier to visualize and interpret than `log returns`.  

We expected to see a high correlation between these delays and the distances separating exchanges. For example, the delays between `NYSE` and `Euronext` should be higher than `NYSE` and `Nasdaq`. When analyzing these delays over multiple years we also expect the delays to:
1. Decrease over time due to the increase in hardware capabilities. More specifically, Moore's law tells us that the transmission speed of information doubles every year. Thus, the delays should, theoratically, decay exponentially over time.
2. Increase with the physical distance between the exchanges.
