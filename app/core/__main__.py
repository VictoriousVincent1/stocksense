"""
Core package initializer for StockSense AI with modern GUI, charts, and multiple tickers.

Run with:
    python -m app.core
"""

from tkinter import Tk, Button, Text, Scrollbar, Entry, Label, END, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib.ticker import MaxNLocator

from .stock_analyzer import StockAnalyzer
from .portfolio_manager import PortfolioManager
from .backtester import Backtester
from .news_sources.newsapi import NewsAPI
from .news_sources.bloomberg import BloombergNews
from .news_sources.reuters import ReutersNews

# Use a soft built-in style
plt.style.use('ggplot')


class CoreTestGUI:
    def __init__(self, master):
        self.master = master
        master.title("StockSense AI Core Test")
        master.geometry("1200x800")
        master.configure(bg="#f0f4f8")  # calm background

        # Top frame for ticker input and buttons
        top_frame = Frame(master, bg="#f0f4f8")
        top_frame.pack(side="top", fill="x", pady=10)

        Label(top_frame, text="Enter tickers (comma-separated):", bg="#f0f4f8", font=("Arial", 12)).pack(side="left", padx=5)
        self.ticker_entry = Entry(top_frame, width=50, font=("Arial", 12))
        self.ticker_entry.insert(0, "AAPL,NVDA,AMZN,GOOGL")
        self.ticker_entry.pack(side="left", padx=5)

        # Buttons
        Button(top_frame, text="Run Full Analysis", command=self.run_full_analysis, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        Button(top_frame, text="Predict Next Move", command=self.run_prediction, bg="#2196F3", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        Button(top_frame, text="Run News Sentiment", command=self.run_news_sentiment, bg="#FF9800", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        Button(top_frame, text="Test Portfolio", command=self.run_portfolio, bg="#9C27B0", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        Button(top_frame, text="Run Backtester", command=self.run_backtester, bg="#607D8B", fg="white", font=("Arial", 10)).pack(side="left", padx=5)

        # Bottom frame for text output
        bottom_frame = Frame(master)
        bottom_frame.pack(side="bottom", fill="both", expand=True)

        # Text box with scrollbar
        self.text = Text(bottom_frame, wrap="word", height=15, width=120, font=("Consolas", 10))
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(bottom_frame, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

        # Portfolio manager
        self.portfolio = PortfolioManager(starting_balance=5000)

        # Frame for charts
        self.chart_frame = Frame(master, bg="#f0f4f8")
        self.chart_frame.pack(side="top", fill="both", expand=True)

    def append_text(self, msg):
        self.text.insert(END, msg + "\n")
        self.text.see(END)

    def get_tickers(self):
        tickers = self.ticker_entry.get().split(",")
        return [t.strip().upper() for t in tickers if t.strip()]

    def plot_stock(self, df, ticker, pred_series=None):
        # Clear previous charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(10, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(df['Date'], df['Close'], label=f'{ticker} Close', color='#4CAF50', linewidth=2)
        if pred_series is not None:
            ax.plot(df['Date'], pred_series, label='AI Prediction', color='#FF5722', linestyle='--', linewidth=2)

        ax.set_title(f"{ticker} Price Chart", fontsize=12)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.legend()
        ax.grid(True)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6))

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def run_full_analysis(self):
        self.append_text("=== Running Full Analysis ===")
        for ticker in self.get_tickers():
            self.append_text(f"\n--- {ticker} ---")
            analyzer = StockAnalyzer(ticker)
            df, acc = analyzer.analyze()
            self.append_text(f"Model Accuracy: {acc:.2f}")
            self.append_text(f"Last 2 rows:\n{df.tail(2)}")
            # Optionally plot AI prediction series
            try:
                pred_series = df['Close'].shift(1)  # Example: shift for visualization
                self.plot_stock(df, ticker, pred_series)
            except Exception:
                self.plot_stock(df, ticker)

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
