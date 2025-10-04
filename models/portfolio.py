from datetime import datetime
from extensions import db


class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False, index=True)
    
    quantity = db.Column(db.Float, nullable=False, default=0)
    average_buy_price = db.Column(db.Float, nullable=False)
    total_invested = db.Column(db.Float, nullable=False)
    
    first_purchase_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='portfolios')
    stock = db.relationship('Stock')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'stock_id', name='unique_user_stock'),
    )

    @property
    def current_value(self):
        if self.stock and self.stock.current_price:
            return self.quantity * self.stock.current_price
        return None

    @property
    def profit_loss(self):
        current_val = self.current_value
        if current_val is not None:
            return current_val - self.total_invested
        return None

    @property
    def profit_loss_percentage(self):
        pl = self.profit_loss
        if pl is not None and self.total_invested != 0:
            return (pl / self.total_invested) * 100
        return None

    def update_position(self, quantity_change, price):
        if quantity_change > 0:
            total_cost = self.total_invested + (quantity_change * price)
            new_quantity = self.quantity + quantity_change
            self.average_buy_price = total_cost / new_quantity if new_quantity > 0 else 0
            self.quantity = new_quantity
            self.total_invested = total_cost
        else:
            sell_quantity = abs(quantity_change)
            if sell_quantity > self.quantity:
                raise ValueError("Cannot sell more than owned quantity")
            
            self.quantity -= sell_quantity
            if self.quantity > 0:
                self.total_invested = self.quantity * self.average_buy_price
            else:
                self.total_invested = 0
                self.average_buy_price = 0

    def __repr__(self):
        return f'<Portfolio User:{self.user_id} Stock:{self.stock.symbol if self.stock else "N/A"}>'
