"""
Flask API server to expose StockSense AI functionality to web frontend.
Save this as: app/api_server.py

Run with:
    python -m app.api_server
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd


import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

from app.core.stock_analyzer import StockAnalyzer
from app.core.portfolio_manager import PortfolioManager
from app.core.backtester import Backtester
from app.core.news_sources.newsapi import NewsAPI
from app.core.news_sources.bloomberg import BloombergNews
from app.core.news_sources.reuters import ReutersNews


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
CORS(app)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/playSpace")
def stockTrade():
    return render_template("index.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

# Global portfolio manager
portfolio = PortfolioManager(starting_balance=5000)


@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    """Full stock analysis with ML prediction."""
    try:
        data = request.json
        tickers = data.get('tickers', [])
        
        results = []
        for ticker in tickers:
            analyzer = StockAnalyzer(ticker)
            df, acc = analyzer.analyze()
            
            # Prepare chart data
            chart_data = df[['Date', 'Close', 'SMA20']].tail(60).to_dict('records')
            for item in chart_data:
                item['Date'] = item['Date'].strftime('%Y-%m-%d')
            
            results.append({
                'ticker': ticker,
                'accuracy': round(acc, 4),
                'latest_price': float(df['Close'].iloc[-1]),
                'latest_date': df['Date'].iloc[-1].strftime('%Y-%m-%d'),
                'rsi': float(df['RSI14'].iloc[-1]) if not pd.isna(df['RSI14'].iloc[-1]) else None,
                'sma20': float(df['SMA20'].iloc[-1]) if not pd.isna(df['SMA20'].iloc[-1]) else None,
                'chart_data': chart_data
            })
        
        return jsonify({'success': True, 'data': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict_movement():
    """Predict next price movement."""
    try:
        data = request.json
        tickers = data.get('tickers', [])
        
        results = []
        for ticker in tickers:
            analyzer = StockAnalyzer(ticker)
            prediction = analyzer.predict_next()
            
            results.append({
                'ticker': ticker,
                'prediction': prediction
            })
        
        return jsonify({'success': True, 'data': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze news sentiment."""
    try:
        data = request.json
        tickers = data.get('tickers', [])
        
        results = []
        for ticker in tickers:
            analyzer = StockAnalyzer(ticker)
            #articles = (
            #    NewsAPI().fetch_news(ticker)
                #+ BloombergNews().fetch_news(ticker)
                #+ ReutersNews().fetch_news(ticker)
            #)
            articles = NewsAPI().fetch_news(ticker)
            sentiment_results = analyzer.analyze_sentiment(articles)
            
            avg_sentiment = sum(sentiment_results.values()) / len(sentiment_results) if sentiment_results else 0
            
            results.append({
                'ticker': ticker,
                'average_sentiment': round(avg_sentiment, 4),
                'articles': [
                    {'text': text, 'score': round(score, 4)}
                    for text, score in list(sentiment_results.items())[:5]
                ]
            })
        
        return jsonify({'success': True, 'data': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    """Run backtesting strategy."""
    try:
        data = request.json
        tickers = data.get('tickers', [])
        
        results = []
        for ticker in tickers:
            analyzer = StockAnalyzer(ticker)
            df, _ = analyzer.analyze()
            
            backtester = Backtester(df)
            final_balance = backtester.run_sma_strategy()
            
            results.append({
                'ticker': ticker,
                'final_balance': round(final_balance, 2),
                'return_pct': round(((final_balance - 10000) / 10000) * 100, 2)
            })
        
        return jsonify({'success': True, 'data': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/portfolio/buy', methods=['POST'])
def portfolio_buy():
    """Buy stocks."""
    try:
        data = request.json
        ticker = data.get('ticker')
        price = data.get('price')
        shares = data.get('shares')
        
        message = portfolio.buy(ticker, price, shares)
        
        return jsonify({
            'success': True,
            'message': message,
            'balance': round(portfolio.balance, 2),
            'holdings': portfolio.holdings
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/portfolio/sell', methods=['POST'])
def portfolio_sell():
    """Sell stocks."""
    try:
        data = request.json
        ticker = data.get('ticker')
        price = data.get('price')
        shares = data.get('shares')
        
        message = portfolio.sell(ticker, price, shares)
        
        return jsonify({
            'success': True,
            'message': message,
            'balance': round(portfolio.balance, 2),
            'holdings': portfolio.holdings
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/portfolio/status', methods=['GET'])
def portfolio_status():
    """Get portfolio status."""
    return jsonify({
        'success': True,
        'balance': round(portfolio.balance, 2),
        'holdings': portfolio.holdings
    })


if __name__ == '__main__':
    #app.run(debug=True, port=5000)
    app.run(host="0.0.0.0", port=env.get("PORT", 5000))
