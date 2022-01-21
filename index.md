# Abstract
The financial world of equity trading relies on centralized exchanges. These exchanges are disseminated around the globe. Thus, it is possible to trade a share of one given company in multiple regions. Because information speed is bounded, shocks on a given share price might take some time to reach all exchanges.

# Motivation

This study aims to analyse how shocks propagate around exchanges located in different regions of the globe. The goal is to measure how fast price changes are flowing from one exchange to another. We expected to see a high correlation between these delays and the distances separating exchanges. For example, the delays between `NYSE` and `Euronext` should be higher than `NYSE` and `Nasdaq`. When analyzing these delays over multiple years we also expect the delays to follow Moore's law. Indeed, Moore's law tells that the transmission speed of information doubles every year. Thus, the delays should exponentially decay with time.

# Method
To perform the described analysis we compare the evolutions of $$SHELL$$ stock price across multiple exchanges. $$SHELL$$ is an actively traded company (XXX STATS XXX) and has been traded in Amsterdam and at NYSE since 2009, allowing us to have a lot of data across multiple years and distant regions. To compare two given signals $$s1_t$$/$$s2_t$$ (same stock from exchange 1 and 2) we compute multiple correlations on lagged versions of the signals. Each used lag is then associated with a correlation as follows :
| lag(ms)  | associated correlation   |
|---|---|
|.....|....|
|  -1 |  corr($$s1_t$$,$$s2_{t-1}$$) |
|  0 |  corr($$s1_t$$,$$s2_{t}$$) |
|  1 |  corr($$s1_t$$,$$s2_{t+1}$$) |
|.....|....|
Correlations are computed using the Hayashi Yoshida estimator. Once computed the lag associated with the highest correlation is extracted and saved. This operation is repeated every day the stock was traded and for every pair of exchanges available. 
At this point, we obtain a time series of lags (one per day) that are interpreted as transmission delays. 
[ss](#method)


## Interactive visualisation 

[is available at this address](https://murmuring-garden-88123.herokuapp.com/)

> **Note**: this application runs of a free container of ***Heroku***, so it may take a couple of seconds to load.
