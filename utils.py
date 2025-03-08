import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf


# INTERVALS = [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
# PERIODS = [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]

def get_data(ticker, interval='1d', period='10y'):
    data = yf.download(ticker, interval=interval, period=period,
                       rounding=True, multi_level_index=False)
    return data


def price_chart(df, type='candle', volume=True, style='yahoo', title='AAPL Price chart'):
    mpf.plot(df.loc['2024-12-01':], type=type,
             volume=volume, style=style, title=title)

    # mpf turns the grid on, we turn it off for future plots
    plt.rcParams['axes.grid'] = False
