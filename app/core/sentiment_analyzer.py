# app/core/sentiment_analyzer.py

from textblob import TextBlob

class SentimentAnalyzer:
    """Analyzes sentiment of financial news articles."""

    def analyze_article(self, text: str) -> float:
        """
        Returns sentiment polarity (-1 = negative, 0 = neutral, +1 = positive).
        """
        return TextBlob(text).sentiment.polarity

    def analyze_articles(self, articles: list[str]) -> dict:
        results = {}
        for article in articles:
            results[article] = self.analyze_article(article)
        return results
