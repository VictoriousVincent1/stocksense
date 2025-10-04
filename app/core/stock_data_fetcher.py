# Robust data fetching
# app/core/stock_data_fetcher.py
import yfinance as yf
import pandas as pd

class StockDataFetcher:
    """Fetches stock price data from APIs like Yahoo Finance."""

    def __init__(self, ticker: str):
        self.ticker = ticker

    def fetch_historical(self, period="1y", interval="1d") -> pd.DataFrame:
        """
        Fetch historical OHLCV (Open, High, Low, Close, Volume) data.
        """
        stock = yf.Ticker(self.ticker)
        hist = stock.history(period=period, interval=interval)
        return hist.reset_index()

    def fetch_latest_price(self) -> float:
        """Fetch the latest stock price."""
        stock = yf.Ticker(self.ticker)
        price = stock.history(period="1d", interval="1m")["Close"].iloc[-1]
        return float(price)
