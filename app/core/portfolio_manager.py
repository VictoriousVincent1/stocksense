# app/core/portfolio_manager.py

class PortfolioManager:
    """Handles virtual portfolio operations (mock trading)."""

    def __init__(self, starting_balance=10000):
        self.balance = starting_balance
        self.holdings = {}  # {ticker: shares}

    def buy(self, ticker: str, market_price: float, shares: int):
        cost = market_price * shares
        if cost > self.balance:
            raise ValueError("Not enough balance!")
        self.balance -= cost
        self.holdings[ticker] = self.holdings.get(ticker, 0) + shares
        return f"✅ Bought {shares} shares of {ticker} at {market_price}"

    def sell(self, ticker: str, market_price: float, shares: int):
        if ticker not in self.holdings or self.holdings[ticker] < shares:
            raise ValueError("Not enough shares to sell!")
        self.balance += market_price * shares
        self.holdings[ticker] -= shares
        if self.holdings[ticker] == 0:
            del self.holdings[ticker]
        return f"✅ Sold {shares} shares of {ticker} at {market_price}"

    def portfolio_value(self, current_prices: dict):
        total = self.balance
        for ticker, shares in self.holdings.items():
            total += shares * current_prices.get(ticker, 0)
        return total
