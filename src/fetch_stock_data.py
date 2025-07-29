"""
Module: fetch_stock_data
Purpose: Fetch historical and intraday stock price data using Yahoo Finance API via yfinance.
Author: Ayobami Samuel Obitade
Date: 2025-07-23
"""

from typing import Optional
import pandas as pd
import yfinance as yf


def fetch_historical_prices(
    ticker: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Fetch historical stock price data for a given ticker.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        start_date (Optional[str]): Start date in 'YYYY-MM-DD' format (inclusive).
        end_date (Optional[str]): End date in 'YYYY-MM-DD' format (inclusive).
        interval (str): Data interval. Options include '1d', '1h', '5m', etc.

    Returns:
        pd.DataFrame: DataFrame containing stock price data with columns like
                      ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'] indexed by datetime.
    """
    yf_ticker = yf.Ticker(ticker)
    df = yf_ticker.history(start=start_date, end=end_date, interval=interval)
    df.reset_index(inplace=True)
    return df


def save_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Save DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save.
        filepath (str): Path to save the CSV file.
    """
    df.to_csv(filepath, index=False)


if __name__ == "__main__":
    # Example usage
    ticker_symbol: str = "AAPL"
    start: str = "2023-01-01"
    end: str = "2024-01-01"
    output_csv_path: str = "data/historical_prices.csv"

    print(f"Fetching historical prices for {ticker_symbol} from {start} to {end}...")

    prices_df = fetch_historical_prices(ticker_symbol, start, end)
    print(f"Data fetched: {prices_df.shape[0]} rows.")

    print(f"Saving data to {output_csv_path}...")
    save_to_csv(prices_df, output_csv_path)

    print("Done.")
