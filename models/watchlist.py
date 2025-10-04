from datetime import datetime
from extensions import db


class Watchlist(db.Model):
    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False, index=True)
    
    notes = db.Column(db.Text)
    target_price = db.Column(db.Float)
    alert_enabled = db.Column(db.Boolean, default=False)
    alert_price_above = db.Column(db.Float)
    alert_price_below = db.Column(db.Float)
    
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='watchlists')
    stock = db.relationship('Stock', back_populates='watchlist_items')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'stock_id', name='unique_user_watchlist_stock'),
    )

    @property
    def current_price(self):
        return self.stock.current_price if self.stock else None

    @property
    def should_trigger_alert(self):
        if not self.alert_enabled or not self.current_price:
            return False
        
        triggers = []
        
        if self.alert_price_above and self.current_price >= self.alert_price_above:
            triggers.append(f"Price above ${self.alert_price_above}")
        
        if self.alert_price_below and self.current_price <= self.alert_price_below:
            triggers.append(f"Price below ${self.alert_price_below}")
        
        return triggers if triggers else False

    def __repr__(self):
        return f'<Watchlist User:{self.user_id} Stock:{self.stock.symbol if self.stock else "N/A"}>'
