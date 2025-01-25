import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_ta as ta


# INTERVALS = [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
# PERIODS = [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]


def get_data(ticker, interval='1d', period='10y'):
    data = yf.download(ticker, interval=interval, period=period)
    data['Datetime'] = data.index
    data.drop(columns=['Adj Close'], inplace=True)
    data = data[['Datetime', 'Volume', 'Open', 'High', 'Low', 'Close']]
    return data


def price_chart(tickers, interval='1d', period='10y'):
    prices = []
    for ticker in tickers:
        data = get_data(ticker, interval, period)
        prices.append(data['Close'])
    df = pd.concat(prices, axis=1)
    df.columns = tickers
    df.plot()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
    plt.title('Price Chart')
    plt.show()

