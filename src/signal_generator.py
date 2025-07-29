# signal_generator.py
"""
Module: signal_generator
Purpose: Generate simple trading signals based on price data and sentiment scores.
Author: Your Name
Date: 2025-07-23
"""

from typing import Optional
import pandas as pd
import numpy as np


def calculate_moving_average(
    df: pd.DataFrame, column: str = "Close", window: int = 20
) -> pd.Series:
    """
    Calculate the moving average of a specified column.

    Args:
        df (pd.DataFrame): DataFrame with stock price data.
        column (str): Column name to calculate the moving average on.
        window (int): Number of periods for moving average.

    Returns:
        pd.Series: Moving average values.
    """
    return df[column].rolling(window=window).mean()


def generate_signals(
    df: pd.DataFrame,
    sentiment_col: str = "avg_compound_sentiment",
    sentiment_threshold: float = 0.05,
    short_ma_window: int = 20,
    long_ma_window: int = 50,
) -> pd.DataFrame:
    """
    Generate buy/sell/hold trading signals based on moving averages and sentiment.

    Strategy:
    - Buy signal (1) when short-term MA crosses above long-term MA and sentiment > threshold.
    - Sell signal (-1) when short-term MA crosses below long-term MA and sentiment < -threshold.
    - Hold signal (0) otherwise.

    Args:
        df (pd.DataFrame): DataFrame with stock prices and sentiment scores.
        sentiment_col (str): Column name for sentiment scores.
        sentiment_threshold (float): Threshold to consider sentiment as positive/negative.
        short_ma_window (int): Window size for short-term moving average.
        long_ma_window (int): Window size for long-term moving average.

    Returns:
        pd.DataFrame: DataFrame with a new 'signal' column added.
    """
    df = df.copy()

    # Calculate moving averages
    df["short_ma"] = calculate_moving_average(df, window=short_ma_window)
    df["long_ma"] = calculate_moving_average(df, window=long_ma_window)

    # Initialize signal column with 0 (hold)
    df["signal"] = 0

    # Generate signals based on crossover and sentiment
    for i in range(1, len(df)):
        prev_short_ma = df.loc[i - 1, "short_ma"]
        prev_long_ma = df.loc[i - 1, "long_ma"]
        curr_short_ma = df.loc[i, "short_ma"]
        curr_long_ma = df.loc[i, "long_ma"]
        sentiment = df.loc[i, sentiment_col]

        # Check if moving averages are not NaN (enough data)
        if np.isnan([prev_short_ma, prev_long_ma, curr_short_ma, curr_long_ma]).any():
            df.loc[i, "signal"] = 0
            continue

        # Buy signal: short MA crosses above long MA AND positive sentiment above threshold
        if (prev_short_ma <= prev_long_ma) and (curr_short_ma > curr_long_ma) and (sentiment > sentiment_threshold):
            df.loc[i, "signal"] = 1

        # Sell signal: short MA crosses below long MA AND negative sentiment below negative threshold
        elif (prev_short_ma >= prev_long_ma) and (curr_short_ma < curr_long_ma) and (sentiment < -sentiment_threshold):
            df.loc[i, "signal"] = -1

        else:
            df.loc[i, "signal"] = 0

    return df
