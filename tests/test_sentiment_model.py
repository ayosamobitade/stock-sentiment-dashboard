"""
Unit tests for sentiment_model.py
Author: Your Name
Date: 2025-07-23
"""

import unittest
from sentiment_model import VaderSentimentAnalyzer


class TestVaderSentimentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = VaderSentimentAnalyzer()

    def test_analyze_text_returns_dict_with_keys(self):
        text = "I love this product!"
        result = self.analyzer.analyze_text(text)
        expected_keys = {"neg", "neu", "pos", "compound"}
        self.assertIsInstance(result, dict)
        self.assertTrue(expected_keys.issubset(result.keys()))

    def test_analyze_text_compound_score_range(self):
        positive_text = "This is fantastic!"
        negative_text = "This is terrible!"
        neutral_text = "It is a table."

        pos_score = self.analyzer.analyze_text(positive_text)["compound"]
        neg_score = self.analyzer.analyze_text(negative_text)["compound"]
        neu_score = self.analyzer.analyze_text(neutral_text)["compound"]

        self.assertGreater(pos_score, 0.5)
        self.assertLess(neg_score, -0.5)
        self.assertAlmostEqual(neu_score, 0, delta=0.2)

    def test_analyze_series_returns_dataframe(self):
        import pandas as pd

        texts = pd.Series(
            ["I love it!", "I hate it!", "It's okay."]
        )
        df_scores = self.analyzer.analyze_series(texts)
        self.assertEqual(df_scores.shape[0], len(texts))
        self.assertIn("compound", df_scores.columns)
        self.assertIn("pos", df_scores.columns)


if __name__ == "__main__":
    unittest.main()
