import pandas as pd
import numpy as np
import pandas_ta as ta
import os
import datetime as dt
from sklearn.preprocessing import MinMaxScaler

from src.config import (
    MA_WINDOW_SIZES, VOL_WINDOW_SIZES, BOLLINGER_WINDOW, BOLLINGER_STD,
    RSI_WINDOW, MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    PROCESSED_DATA_DIR, NORMALIZED_DATA_DIR
)


def compute_technical_indicators(data):
    """
    Calculate technical indicators for the given stock data
    """

    df = data.copy()

    for window in MA_WINDOW_SIZES:
        df[f'ema_{window}'] = ta.ema(df['close'], length=window)

    bollinger = ta.bbands(
        df['close'], length=BOLLINGER_WINDOW, std=BOLLINGER_STD)
    df = pd.concat([df, bollinger], axis=1)

    df[f'rsi_{RSI_WINDOW}'] = ta.rsi(df['close'], length=RSI_WINDOW)

    macd = ta.macd(df['close'], fast=MACD_FAST,
                   slow=MACD_SLOW, signal=MACD_SIGNAL)
    df = pd.concat([df, macd], axis=1)

    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)

    df['cci'] = ta.cci(df['high'], df['low'], df['close'], length=20)

    df['roc'] = ta.roc(df['close'], length=10)

    df['obv'] = ta.obv(df['close'], df['volume'])


    return df


def generate_summary_statistics(data):
    """
    Generate summary statistics for a given dataframe
    """

    df = data.copy()

    df['daily_return'] = df['close'].pct_change()

    df['daily_log_return'] = np.log1p(df['close'].pct_change())

    df['cum_return'] = (1 + df['daily_return']).cumprod() - 1

    df['cum_log_return'] = np.exp(df["daily_log_return"].cumsum()) - 1

    for window in VOL_WINDOW_SIZES:
        df[f'volatility_{window}d'] = df['daily_log_return'].rolling(
            window=window).std()

    df['volume_change'] = df['volume'].pct_change()

    df['high_low_range'] = (df['high'] - df['low']) / df['close']


    return df


def create_feature_sets(data, save=False, ticker=None):
    """
    Create comprehensive feature sets for machine learning
    """

    df_technical = compute_technical_indicators(data)
    df_features = generate_summary_statistics(df_technical)

    df_features = df_features.dropna()

    if save and ticker:
        ticker_dir = os.path.join(PROCESSED_DATA_DIR, ticker)
        os.makedirs(ticker_dir, exist_ok=True)

        timestamp = dt.datetime.today().strftime("%Y-%m-%d")
        filename = f"{ticker}_features_{timestamp}.csv"
        filepath = os.path.join(ticker_dir, filename)
        df_features.to_csv(filepath)
        print(f"Saved feature set for {ticker} to {filepath}")

    return df_features


def normalize_features(features, save=False, ticker=None,exclude_cols=None):
    """
    Normalize features using Min-Max scaling
    """

    df = features.copy()

    if exclude_cols is None:
        exclude_cols = []

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    cols_to_normalize = [
        col for col in numeric_cols if col not in exclude_cols]

    scaler = MinMaxScaler()
    df[cols_to_normalize] = scaler.fit_transform(df[cols_to_normalize])

    if save and ticker:
        ticker_dir = os.path.join(NORMALIZED_DATA_DIR, ticker)
        os.makedirs(ticker_dir, exist_ok=True)

        timestamp = dt.datetime.today().strftime("%Y-%m-%d")
        filename = f"{ticker}_features_{timestamp}.csv"
        filepath = os.path.join(ticker_dir, filename)
        df.to_csv(filepath)
        print(f"Saved normalized feature set for {ticker} to {filepath}")

    return df, scaler
