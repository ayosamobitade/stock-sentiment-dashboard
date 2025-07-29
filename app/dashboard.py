"""
Streamlit dashboard for real-time stock price tracking combined with sentiment analysis.
Author: Your Name
Date: 2025-07-23
"""

from typing import Optional
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from src.fetch_stock_data import fetch_historical_prices
from src.fetch_tweets import fetch_tweets
from src.sentiment_model import VaderSentimentAnalyzer
from src.signal_generator import generate_signals


def load_data(
    ticker: str,
    start_date: Optional[str],
    end_date: Optional[str],
    max_tweets: int = 500,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load stock prices and fetch tweets for sentiment analysis.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (Optional[str]): Start date string 'YYYY-MM-DD'.
        end_date (Optional[str]): End date string 'YYYY-MM-DD'.
        max_tweets (int): Max tweets to fetch for sentiment.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Stock prices and tweets DataFrames.
    """
    stock_df = fetch_historical_prices(ticker, start_date, end_date)
    query = f"{ticker} stock -filter:retweets lang:en"
    tweets_df = fetch_tweets(query, max_tweets=max_tweets, since=start_date, until=end_date)
    return stock_df, tweets_df


def analyze_sentiment(tweets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze sentiment scores of tweets using VADER.

    Args:
        tweets_df (pd.DataFrame): Tweets DataFrame with 'content' column.

    Returns:
        pd.DataFrame: Tweets DataFrame with added sentiment columns.
    """
    analyzer = VaderSentimentAnalyzer()
    sentiment_scores = analyzer.analyze_series(tweets_df["content"])
    tweets_with_sentiment = pd.concat([tweets_df.reset_index(drop=True), sentiment_scores], axis=1)
    return tweets_with_sentiment


def aggregate_sentiment(tweets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate average daily compound sentiment scores.

    Args:
        tweets_df (pd.DataFrame): Tweets DataFrame with 'date' and 'compound'.

    Returns:
        pd.DataFrame: DataFrame with 'Date' and 'avg_compound_sentiment'.
    """
    daily_sentiment = tweets_df.groupby(tweets_df["date"].dt.date)["compound"].mean().reset_index()
    daily_sentiment.rename(columns={"date": "Date", "compound": "avg_compound_sentiment"}, inplace=True)
    daily_sentiment["Date"] = pd.to_datetime(daily_sentiment["Date"])
    return daily_sentiment


def plot_price_and_signals(df: pd.DataFrame, ticker: str) -> None:
    """
    Plot stock close prices with buy/sell signals using Plotly.

    Args:
        df (pd.DataFrame): DataFrame with price and 'signal' column.
        ticker (str): Stock ticker symbol.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Close Price"))

    buys = df[df["signal"] == 1]
    sells = df[df["signal"] == -1]

    fig.add_trace(
        go.Scatter(
            x=buys["Date"],
            y=buys["Close"],
            mode="markers",
            marker=dict(symbol="triangle-up", color="green", size=12),
            name="Buy Signal",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=sells["Date"],
            y=sells["Close"],
            mode="markers",
            marker=dict(symbol="triangle-down", color="red", size=12),
            name="Sell Signal",
        )
    )

    fig.update_layout(
        title=f"{ticker} Close Price with Trading Signals",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend=dict(x=0, y=1),
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.title("📈 Real-Time Stock Price & Sentiment Dashboard")

    # Sidebar inputs
    ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()
    today = datetime.today()
    default_start = (today - timedelta(days=90)).strftime("%Y-%m-%d")

    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime(default_start))
    end_date = st.sidebar.date_input("End Date", value=today)

    max_tweets = st.sidebar.slider("Max Tweets to Fetch", min_value=100, max_value=2000, value=500, step=100)

    # Validate dates
    if start_date > end_date:
        st.error("Error: Start date must be before end date.")
        return

    with st.spinner("Loading data..."):
        stock_df, tweets_df = load_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), max_tweets)

    if stock_df.empty:
        st.error(f"No stock data found for {ticker}. Please try a different ticker or date range.")
        return

    if tweets_df.empty:
        st.warning("No tweets found for the selected query and date range.")

    st.subheader(f"Stock Price Data for {ticker}")
    st.dataframe(stock_df.tail())

    if not tweets_df.empty:
        tweets_df["date"] = pd.to_datetime(tweets_df["date"])
        tweets_with_sentiment = analyze_sentiment(tweets_df)

        st.subheader("Sample Tweets with Sentiment Scores")
        st.dataframe(tweets_with_sentiment[["date", "username", "content", "compound"]].head(10))

        daily_sentiment_df = aggregate_sentiment(tweets_with_sentiment)

        # Merge price and sentiment
        combined_df = pd.merge(stock_df, daily_sentiment_df, on="Date", how="left")
        combined_df["avg_compound_sentiment"].fillna(method="ffill", inplace=True)

        # Calculate daily returns
        combined_df["daily_return"] = combined_df["Close"].pct_change() * 100

        # Generate signals
        combined_df = generate_signals(combined_df)

        st.subheader("Price Chart with Buy/Sell Signals")
        plot_price_and_signals(combined_df, ticker)
    else:
        st.info("No sentiment data to analyze.")

    st.markdown("---")
    st.markdown("Dashboard built with Streamlit and Python.")


if __name__ == "__main__":
    main()
