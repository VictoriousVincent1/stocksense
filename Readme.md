# 📈 StockSense AI
![StockSense Logo](Dashboard_images/logo.png)

**🎥 Watch the Demo:** [StockSense AI - YouTube](https://www.youtube.com/watch?v=V7fqIPa9M1k)

StockSense AI is a modern, interactive web platform for AI-driven stock prediction, portfolio management, news sentiment analysis, and backtesting. Built for traders, students, and finance enthusiasts, it uses machine learning models (scikit-learn), yfinance, pandas, and a Flask backend.  

![StockSense Dashboard](Dashboard_images/login.png)
![StockSense Dashboard](Dashboard_images/Portfolio.png)
![StockSense Dashboard](Dashboard_images/charts.png)
![StockSense Dashboard](Dashboard_images/Prediction.png)
![StockSense Dashboard](Dashboard_images/News.png)
![StockSense Dashboard](Dashboard_images/Backtest.png)
![StockSense Dashboard](Dashboard_images/ai_agent.png)
---

## Features

- 📊 Multi-ticker technical and ML analysis with real-time charting  
- 🤖 Predict price movements and show model accuracy  
- 📰 News sentiment analysis using NewsAPI, Bloomberg, Reuters  
- 💼 Portfolio simulation with buy/sell at market price  
- 🧪 Backtest classic strategies  
- 🔒 Modern authentication (Auth0) for secure user sessions  
- 🚦 Dashboard UI with AI assistant powered by Gemini Flash 2.5  

---

## Getting Started

1. Clone this repository.
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Start the backend server:  
   `python -m app.api_server`
4. Open your browser at [http://localhost:5000](http://localhost:5000) and log in!

---

## Technologies Used

- Flask, Flask-SQLAlchemy, Flask-Login, flask-cors
- yfinance, pandas, scikit-learn, matplotlib
- Authlib, python-dotenv, requests
- Auth0 (for secure login)
- Gemini Flash 2.5 for AI assistant

---

## License

MIT

---

*Built for HackUTA 2025*

