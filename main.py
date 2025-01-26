import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_ta as ta
import mplfinance as mpf


# INTERVALS = [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
# PERIODS = [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]


def get_data(ticker, interval='1d', period='10y'):
    data = yf.download(ticker, interval=interval, period=period,
                       rounding=True, multi_level_index=False)
    data.drop(columns=['Adj Close'], inplace=True)
    data = data[['Volume', 'Open', 'High', 'Low', 'Close']]
    return data


def price_chart(df, type='candle', volume=True, style='yahoo', title='Price chart'):
    df = df.copy()
    # df.columns = df.columns.droplevel(1)
    mpf.plot(df.iloc[-100:, :], type=type,
             volume=volume, style=style, title=title)

aapl = get_data('AAPL')
price_chart(aapl)
