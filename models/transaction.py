from datetime import datetime
from extensions import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False, index=True)
    
    transaction_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    commission = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = db.Column(db.String(20), default='completed', nullable=False)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='transactions')
    stock = db.relationship('Stock', back_populates='transactions')

    @property
    def net_amount(self):
        if self.transaction_type == 'BUY':
            return self.total_amount + self.commission + self.tax
        else:
            return self.total_amount - self.commission - self.tax

    @property
    def is_buy(self):
        return self.transaction_type.upper() == 'BUY'

    @property
    def is_sell(self):
        return self.transaction_type.upper() == 'SELL'

    def __repr__(self):
        return f'<Transaction {self.transaction_type} {self.quantity} {self.stock.symbol if self.stock else "N/A"}>'
