"""
Module: sentiment_model
Purpose: Provide NLP sentiment analysis functions using VADER and optionally BERT.
Author: Your Name
Date: 2025-07-23
"""

from typing import List, Union
import pandas as pd

# VADER for lexicon-based sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Transformers for BERT (optional, heavier model)
from transformers import pipeline


class VaderSentimentAnalyzer:
    """
    Wrapper class for VADER sentiment analysis.
    """

    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> dict:
        """
        Analyze sentiment scores for a single text.

        Args:
            text (str): Input text string.

        Returns:
            dict: Dictionary with keys 'neg', 'neu', 'pos', 'compound'.
        """
        return self.analyzer.polarity_scores(text)

    def analyze_series(self, texts: pd.Series) -> pd.DataFrame:
        """
        Analyze sentiment scores for a Pandas Series of texts.

        Args:
            texts (pd.Series): Series of text strings.

        Returns:
            pd.DataFrame: DataFrame with sentiment scores columns.
        """
        scores = texts.apply(self.analyze_text)
        df_scores = pd.json_normalize(scores)
        return df_scores


class BertSentimentAnalyzer:
    """
    Wrapper class for BERT-based sentiment analysis using Hugging Face pipeline.
    Note: Requires `transformers` package and downloading model weights (~400MB).
    """

    def __init__(self, model_name: str = "nlptown/bert-base-multilingual-uncased-sentiment") -> None:
        """
        Initialize BERT sentiment analysis pipeline.

        Args:
            model_name (str): Hugging Face model name.
        """
        self.classifier = pipeline("sentiment-analysis", model=model_name)

    def analyze_text(self, text: str) -> dict:
        """
        Analyze sentiment label and score for a single text.

        Args:
            text (str): Input text string.

        Returns:
            dict: Dictionary with 'label' and 'score'.
        """
        result = self.classifier(text)[0]
        return result

    def analyze_list(self, texts: List[str]) -> List[dict]:
        """
        Analyze a list of texts.

        Args:
            texts (List[str]): List of text strings.

        Returns:
            List[dict]: List of sentiment result dicts.
        """
        return self.classifier(texts)


# Example usage functions

def analyze_with_vader(texts: Union[List[str], pd.Series]) -> pd.DataFrame:
    """
    Convenience function to analyze a batch of texts using VADER.

    Args:
        texts (Union[List[str], pd.Series]): List or Series of texts.

    Returns:
        pd.DataFrame: DataFrame with sentiment scores.
    """
    analyzer = VaderSentimentAnalyzer()
    if isinstance(texts, list):
        texts = pd.Series(texts)
    return analyzer.analyze_series(texts)


if __name__ == "__main__":
    # Quick test with sample sentences
    sample_texts = pd.Series(
        [
            "I love this stock! It's going up.",
            "This is terrible news, I'm worried.",
            "The stock price is stable today.",
        ]
    )

    print("VADER Sentiment Analysis Results:")
    vader_results = analyze_with_vader(sample_texts)
    print(vader_results)

    # Uncomment below for BERT testing (requires transformers installed)
    # bert_analyzer = BertSentimentAnalyzer()
    # bert_results = bert_analyzer.analyze_list(sample_texts.tolist())
    # print("BERT Sentiment Analysis Results:")
    # print(bert_results)
