import yfinance as yf
import pandas as pd
import numpy as np
import os
import datetime as dt
from pathlib import Path

from src.config import RAW_DATA_DIR, NORMALIZED_DATA_DIR, PROCESSED_DATA_DIR, DEFAULT_PERIOD, DEFAULT_INTERVAL


def get_data(ticker, interval=DEFAULT_INTERVAL, period=DEFAULT_PERIOD):
    """
    Download historical stock data from Yahoo Finance
    """
    data = yf.download(ticker, interval=interval, period=period,
                       auto_adjust=True, multi_level_index=False)
    return data


def download_raw(ticker, interval=DEFAULT_INTERVAL, period=DEFAULT_PERIOD, save=False):
    """
    Download raw stock data from Yahoo Finance for a single ticker and optionally save to the raw data directory.
    Returns a single pandas DataFrame for the given ticker.
    """
    if not isinstance(ticker, str):
        raise TypeError("ticker must be a string")

    print(f"Downloading data for {ticker}...")
    data = get_data(ticker, interval, period)

    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    data.columns = data.columns.str.lower()

    data = data[['open', 'high', 'low', 'close', 'volume']]

    if save:
        ticker_dir = os.path.join(RAW_DATA_DIR, ticker)
        os.makedirs(ticker_dir, exist_ok=True)

        timestamp = dt.datetime.today().strftime("%Y-%m-%d")
        filename = f"{ticker}_{period}_{timestamp}.csv"
        filepath = os.path.join(ticker_dir, filename)
        data.to_csv(filepath)
        print(f"Saved raw data for {ticker} to {filepath}")

    return data


def compute_returns(data):
    """
    Process raw data and prepare it for modeling, save to processed directory
    """

    data['daily_return'] = data['close'].pct_change()
    data['log_return'] = np.log1p(data['close'].pct_change())
    data['tot_return'] = (1 + data['log_return']).cumprod()
    data['volatility_20d'] = data['log_return'].rolling(window=20).std()

    data = data.dropna()

    return data


def get_latest_file(directory, pattern):
    """
    Get the latest file in a directory that matches a pattern
    """
    files = list(Path(directory).glob(pattern))
    if not files:
        return None

    return str(max(files, key=os.path.getmtime))


def load_latest_data(ticker, data_type='raw'):
    """
    Load the latest data file for a ticker
    """

    if data_type == 'raw':
        data_dir = os.path.join(RAW_DATA_DIR, ticker)
        pattern = f"{ticker}_*.csv"
    elif data_type == 'processed':
        data_dir = os.path.join(PROCESSED_DATA_DIR, ticker)
        pattern = f"{ticker}_processed_*.csv"
    elif data_type == 'normalized':
        data_dir = os.path.join(NORMALIZED_DATA_DIR, ticker)
        pattern = f"{ticker}_normalized_*.csv"
    else:
        raise ValueError(f"Invalid data_type: {data_type}")

    filepath = get_latest_file(data_dir, pattern)

    if not filepath:
        raise FileNotFoundError(f"No {data_type} data found for {ticker}")

    data = pd.read_csv(filepath, index_col=0, parse_dates=True)

    return data
