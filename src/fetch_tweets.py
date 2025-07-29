"""
Module: fetch_tweets
Purpose: Fetch tweets related to a stock ticker or keyword using snscrape.
Author: Ayobami Samuel Obitade
Date: 2025-07-23
"""

from typing import List, Optional
import pandas as pd
import snscrape.modules.twitter as sntwitter


def fetch_tweets(
    query: str,
    max_tweets: int = 1000,
    since: Optional[str] = None,
    until: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch tweets matching a query using snscrape.

    Args:
        query (str): Search query string (e.g., 'AAPL stock').
        max_tweets (int): Maximum number of tweets to fetch.
        since (Optional[str]): Start date filter in 'YYYY-MM-DD' format (inclusive).
        until (Optional[str]): End date filter in 'YYYY-MM-DD' format (exclusive).

    Returns:
        pd.DataFrame: DataFrame containing tweet data with columns:
                      ['date', 'username', 'content', 'url', 'retweetCount', 'likeCount']
    """
    # Build the search query with date filters if provided
    date_filter = ""
    if since:
        date_filter += f" since:{since}"
    if until:
        date_filter += f" until:{until}"
    full_query = query + date_filter

    tweets_list = []

    scraper = sntwitter.TwitterSearchScraper(full_query)
    for i, tweet in enumerate(scraper.get_items()):
        if i >= max_tweets:
            break
        tweets_list.append(
            {
                "date": tweet.date,
                "username": tweet.user.username,
                "content": tweet.content,
                "url": tweet.url,
                "retweetCount": tweet.retweetCount,
                "likeCount": tweet.likeCount,
            }
        )

    df = pd.DataFrame(tweets_list)
    return df


def save_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Save DataFrame to CSV.

    Args:
        df (pd.DataFrame): DataFrame to save.
        filepath (str): CSV file path.
    """
    df.to_csv(filepath, index=False)


if __name__ == "__main__":
    # Example usage
    search_query: str = "AAPL stock"
    max_tweets_to_fetch: int = 500
    since_date: str = "2024-01-01"
    until_date: str = "2024-07-01"
    output_csv_path: str = "data/tweets_aapl.csv"

    print(f"Fetching tweets for query: '{search_query}'...")
    tweets_df = fetch_tweets(search_query, max_tweets_to_fetch, since_date, until_date)
    print(f"Fetched {tweets_df.shape[0]} tweets.")

    print(f"Saving tweets to {output_csv_path}...")
    save_to_csv(tweets_df, output_csv_path)

    print("Done.")
