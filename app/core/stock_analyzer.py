# app/core/stock_analyzer.py

import pandas as pd
from .stock_data_fetcher import StockDataFetcher
from .data_cleaner import DataCleaner
from .technical_indicators import TechnicalIndicators
from .ml_predictor import MLPredictor
from .sentiment_analyzer import SentimentAnalyzer

class StockAnalyzer:
    """Main orchestrator for stock analysis and prediction."""

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.fetcher = StockDataFetcher(ticker)
        self.predictor = MLPredictor()
        self.sentiment = SentimentAnalyzer()

    def analyze(self):
        """Full pipeline: fetch → clean → indicators → ML training."""
        print(f"🔍 Analyzing {self.ticker}...")

        # Step 1: Fetch
        raw_data = self.fetcher.fetch_historical(period="6mo", interval="1d")

        # Step 2: Clean
        df = DataCleaner.clean(raw_data)

        # Step 3: Add indicators
        df["SMA20"] = TechnicalIndicators.moving_average(df, 20)
        df["RSI14"] = TechnicalIndicators.rsi(df, 14)

        # Step 4: Train ML
        acc = self.predictor.train_model(df)

        print(f"✅ Model trained with accuracy: {acc:.2f}")
        return df, acc

    def predict_next(self):
        """Predicts the next stock movement."""
        df = self.fetcher.fetch_historical(period="1mo", interval="1d")
        df = DataCleaner.clean(df)
        self.predictor.train_model(df)
        latest = df[["Open", "High", "Low", "Close", "Volume"]].iloc[[-1]]


        prediction = self.predictor.predict_next(latest)
        return prediction

    def analyze_sentiment(self, articles: list[str]):
        """Analyze sentiment of news headlines/articles."""
        return self.sentiment.analyze_articles(articles)
