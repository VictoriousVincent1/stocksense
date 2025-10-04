# Strategy backtesting
# app/core/backtester.py

import pandas as pd

class Backtester:
    """Simple backtesting for trading strategies."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.balance = 10000
        self.shares = 0

    def run_sma_strategy(self, short_window=20, long_window=50):
        """Simple SMA crossover strategy."""
        self.df["SMA_short"] = self.df["Close"].rolling(short_window).mean()
        self.df["SMA_long"] = self.df["Close"].rolling(long_window).mean()

        for i in range(len(self.df)):
            row = self.df.iloc[i]
            price = row["Close"]

            if row["SMA_short"] > row["SMA_long"] and self.shares == 0:
                self.shares = self.balance // price
                self.balance -= self.shares * price

            elif row["SMA_short"] < row["SMA_long"] and self.shares > 0:
                self.balance += self.shares * price
                self.shares = 0

        # Final liquidation
        if self.shares > 0:
            self.balance += self.shares * self.df.iloc[-1]["Close"]
            self.shares = 0

        return self.balance
