# Calculate indicators# app/core/technical_indicators.py
import pandas as pd

class TechnicalIndicators:
    """Generates technical indicators for stock analysis."""

    @staticmethod
    def moving_average(df: pd.DataFrame, window: int = 20) -> pd.Series:
        return df["Close"].rolling(window=window).mean()

    @staticmethod
    def rsi(df: pd.DataFrame, window: int = 14) -> pd.Series:
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
