"""
Core package initializer for StockSense AI with basic GUI for testing multiple tickers.

Run with:
    python -m app.core
"""

from tkinter import Tk, Button, Text, Scrollbar, Entry, Label, END
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

        # Ticker input
        Label(master, text="Enter tickers (comma-separated):").pack()
        self.ticker_entry = Entry(master, width=50)
        self.ticker_entry.insert(0, "AAPL,NVDA,AMZN,GOOGL")
        self.ticker_entry.pack()

        # Portfolio manager (one per GUI session)
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

    def get_tickers(self):
        tickers = self.ticker_entry.get().split(",")
        return [t.strip().upper() for t in tickers if t.strip()]

    def run_full_analysis(self):
        self.append_text("=== Running Full Analysis ===")
        for ticker in self.get_tickers():
            self.append_text(f"\n--- {ticker} ---")
            analyzer = StockAnalyzer(ticker)
            df, acc = analyzer.analyze()
            self.append_text(f"Model Accuracy: {acc:.2f}")
            self.append_text(f"Last 2 rows:\n{df.tail(2)}")

    def run_prediction(self):
        self.append_text("=== Running Prediction ===")
        for ticker in self.get_tickers():
            analyzer = StockAnalyzer(ticker)
            pred = analyzer.predict_next()
            self.append_text(f"{ticker} Prediction: {pred}")

    def run_news_sentiment(self):
        self.append_text("=== Running News Sentiment ===")
        for ticker in self.get_tickers():
            analyzer = StockAnalyzer(ticker)
            articles = (
                NewsAPI().fetch_news(ticker)
                + BloombergNews().fetch_news(ticker)
                + ReutersNews().fetch_news(ticker)
            )
            results = analyzer.analyze_sentiment(articles)
            self.append_text(f"\n--- {ticker} ---")
            for article, score in results.items():
                self.append_text(f"{article} → Sentiment: {score:.2f}")

    def run_portfolio(self):
        self.append_text("=== Testing Portfolio Buy/Sell ===")
        for ticker in self.get_tickers():
            analyzer = StockAnalyzer(ticker)
            df, _ = analyzer.analyze()
            price = df["Close"].iloc[-1]
            self.append_text(f"\n--- {ticker} ---")
            self.append_text(self.portfolio.buy(ticker, price, 5))
            self.append_text(self.portfolio.sell(ticker, price, 2))
            self.append_text(f"Portfolio Value: {self.portfolio.portfolio_value({ticker: price})}")

    def run_backtester(self):
        self.append_text("=== Running Backtester ===")
        for ticker in self.get_tickers():
            analyzer = StockAnalyzer(ticker)
            df, _ = analyzer.analyze()
            backtester = Backtester(df)
            balance = backtester.run_sma_strategy()
            self.append_text(f"{ticker} Final backtest balance: {balance:.2f}")


def run_core_gui():
    root = Tk()
    gui = CoreTestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_core_gui()
