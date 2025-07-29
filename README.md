# Real-Time Stock Price Dashboard with Sentiment Analysis

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.20.0-orange.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

This project builds a real-time dashboard that tracks live stock prices combined with sentiment analysis from social media (Twitter/Reddit). It provides actionable buy/sell insights by merging financial data with public sentiment.

The dashboard demonstrates:
- Working with financial APIs (Yahoo Finance via `yfinance`)
- Social media data scraping (`snscrape` for Twitter)
- Sentiment analysis using VADER and optionally BERT models
- Simple trading signal generation using moving averages + sentiment
- Interactive visualization with Streamlit and Plotly

---

## Features

- Fetches historical stock price data dynamically
- Scrapes recent tweets related to a stock ticker
- Analyzes sentiment scores from tweets
- Aggregates daily sentiment and correlates with stock returns
- Generates buy, sell, or hold signals based on price & sentiment
- Interactive dashboard with customizable ticker, date range, and tweet volume

---

## Project Structure

```
stock-sentiment-dashboard/
│
├── data/ # Sample datasets (CSV)
│ ├── historical_prices.csv
│ └── sentiment_data.csv
│
├── notebooks/ # Jupyter notebooks for analysis
│ ├── 01_price_analysis.ipynb
│ ├── 02_sentiment_analysis.ipynb
│ └── 03_correlation_and_signals.ipynb
│
├── src/ # Source code modules
│ ├── fetch_stock_data.py
│ ├── fetch_tweets.py
│ ├── sentiment_model.py
│ ├── signal_generator.py
│ └── utils.py
│
├── app/
│ ├── dashboard.py # Streamlit dashboard app
│ └── requirements.txt # Project dependencies
│
├── tests/ # Unit tests
│ └── test_sentiment_model.py
│
├── README.md
└── LICENSE
```
