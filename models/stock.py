from datetime import datetime
from extensions import db


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    exchange = db.Column(db.String(50))
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    market_cap = db.Column(db.BigInteger)
    
    current_price = db.Column(db.Float)
    previous_close = db.Column(db.Float)
    open_price = db.Column(db.Float)
    day_high = db.Column(db.Float)
    day_low = db.Column(db.Float)
    volume = db.Column(db.BigInteger)
    
    pe_ratio = db.Column(db.Float)
    dividend_yield = db.Column(db.Float)
    fifty_two_week_high = db.Column(db.Float)
    fifty_two_week_low = db.Column(db.Float)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    predictions = db.relationship('Prediction', back_populates='stock', lazy='dynamic', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', back_populates='stock', lazy='dynamic', cascade='all, delete-orphan')
    watchlist_items = db.relationship('Watchlist', back_populates='stock', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def price_change(self):
        if self.current_price and self.previous_close:
            return self.current_price - self.previous_close
        return None

    @property
    def price_change_percent(self):
        if self.current_price and self.previous_close and self.previous_close != 0:
            return ((self.current_price - self.previous_close) / self.previous_close) * 100
        return None

    def __repr__(self):
        return f'<Stock {self.symbol}>'
