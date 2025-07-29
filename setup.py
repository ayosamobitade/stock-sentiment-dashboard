from setuptools import setup, find_packages

setup(
    name="stock_sentiment_dashboard",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A real-time stock price dashboard with Twitter sentiment analysis.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stock-sentiment-dashboard",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.22.0",
        "plotly>=5.10.0",
        "streamlit>=1.20.0",
        "yfinance>=0.2.18",
        "snscrape>=0.4.4.20220110",
        "vaderSentiment>=3.3.2",
        "transformers>=4.30.0",
        "torch>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "stock-dashboard=app.dashboard:main",
        ],
    },
)
