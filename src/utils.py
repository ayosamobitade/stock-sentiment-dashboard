"""
Module: utils
Purpose: Utility helper functions used across the stock sentiment dashboard project.
Author: Your Name
Date: 2025-07-23
"""

import os
from typing import Optional
import pandas as pd


def file_exists(filepath: str) -> bool:
    """
    Check if a file exists at the given path.

    Args:
        filepath (str): Path to the file.

    Returns:
        bool: True if file exists, False otherwise.
    """
    return os.path.isfile(filepath)


def read_csv_safe(filepath: str, **kwargs) -> Optional[pd.DataFrame]:
    """
    Safely read a CSV file into a DataFrame. Returns None if file not found or error occurs.

    Args:
        filepath (str): Path to the CSV file.
        **kwargs: Additional keyword arguments for pandas.read_csv.

    Returns:
        Optional[pd.DataFrame]: DataFrame if read successful, None otherwise.
    """
    if not file_exists(filepath):
        print(f"Warning: File not found at {filepath}")
        return None

    try:
        df = pd.read_csv(filepath, **kwargs)
        return df
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def save_dataframe_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Save a DataFrame to CSV with basic error handling.

    Args:
        df (pd.DataFrame): DataFrame to save.
        filepath (str): Destination file path.
    """
    try:
        df.to_csv(filepath, index=False)
        print(f"Saved DataFrame to {filepath}")
    except Exception as e:
        print(f"Failed to save DataFrame to {filepath}: {e}")


def convert_to_datetime(
    df: pd.DataFrame, column: str, errors: str = "raise"
) -> pd.DataFrame:
    """
    Convert a DataFrame column to datetime dtype.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name to convert.
        errors (str): Error handling mode for pd.to_datetime ('raise', 'coerce', 'ignore').

    Returns:
        pd.DataFrame: DataFrame with converted datetime column.
    """
    df[column] = pd.to_datetime(df[column], errors=errors)
    return df
