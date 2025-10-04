"""
Core package initializer for StockSense AI with basic GUI for testing.

Run with:
    python -m app.core
"""

from tkinter import Tk, Button, Text, Scrollbar, END
from .stock_analyzer import StockAnalyzer
from .portfolio_manager import PortfolioManager
from .backtester import Backtester
from .news_sources.newsapi import NewsAPI
from .news_sources.bloomberg import BloombergNews
from .news_sources.reuters import ReutersNews


class CoreTestGUI:
    def __init__(self, master):
        self.master = master
        master.title("StockSense AI Core Test")

        self.ticker = "AAPL"
        self.analyzer = StockAnalyzer(self.ticker)
        self.portfolio = PortfolioManager(starting_balance=5000)

        # Text box with scrollbar
        self.text = Text(master, wrap="word", height=25, width=100)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(master, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

        # Buttons
        Button(master, text="Run Full Analysis", command=self.run_full_analysis).pack()
        Button(master, text="Predict Next Move", command=self.run_prediction).pack()
        Button(master, text="Run News Sentiment", command=self.run_news_sentiment).pack()
        Button(master, text="Test Portfolio Buy/Sell", command=self.run_portfolio).pack()
        Button(master, text="Run Backtester", command=self.run_backtester).pack()

    def append_text(self, msg):
        self.text.insert(END, msg + "\n")
        self.text.see(END)

    def run_full_analysis(self):
        self.append_text("=== Running Full Analysis ===")
        df, acc = self.analyzer.analyze()
        self.append_text(f"Model Accuracy: {acc:.2f}")
        self.append_text(f"Last 2 rows:\n{df.tail(2)}")

    def run_prediction(self):
        self.append_text("=== Running Prediction ===")
        pred = self.analyzer.predict_next()
        self.append_text(f"Prediction for {self.ticker}: {pred}")

    def run_news_sentiment(self):
        self.append_text("=== Running News Sentiment ===")
        articles = (
            NewsAPI().fetch_news(self.ticker)
            + BloombergNews().fetch_news(self.ticker)
            + ReutersNews().fetch_news(self.ticker)
        )
        results = self.analyzer.analyze_sentiment(articles)
        for article, score in results.items():
            self.append_text(f"{article} → Sentiment: {score:.2f}")

    def run_portfolio(self):
        self.append_text("=== Testing Portfolio Buy/Sell ===")
        df, _ = self.analyzer.analyze()
        price = df["Close"].iloc[-1]
        self.append_text(self.portfolio.buy(self.ticker, price, 5))
        self.append_text(self.portfolio.sell(self.ticker, price, 2))
        self.append_text(f"Portfolio Value: {self.portfolio.portfolio_value({self.ticker: price})}")

    def run_backtester(self):
        self.append_text("=== Running Backtester ===")
        df, _ = self.analyzer.analyze()
        backtester = Backtester(df)
        balance = backtester.run_sma_strategy()
        self.append_text(f"Final backtest balance: {balance:.2f}")


def run_core_gui():
    root = Tk()
    gui = CoreTestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_core_gui()
