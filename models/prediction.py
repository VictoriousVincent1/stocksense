from datetime import datetime
from extensions import db


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False, index=True)
    
    prediction_date = db.Column(db.Date, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    actual_price = db.Column(db.Float)
    
    model_name = db.Column(db.String(50), nullable=False)
    model_version = db.Column(db.String(20))
    confidence_score = db.Column(db.Float)
    
    prediction_type = db.Column(db.String(20))
    trend = db.Column(db.String(20))
    
    extra_data = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    stock = db.relationship('Stock', back_populates='predictions')

    @property
    def accuracy(self):
        if self.actual_price and self.predicted_price:
            error = abs(self.actual_price - self.predicted_price)
            accuracy = (1 - (error / self.actual_price)) * 100
            return max(0, min(100, accuracy))
        return None

    @property
    def error_percentage(self):
        if self.actual_price and self.predicted_price and self.actual_price != 0:
            return ((self.predicted_price - self.actual_price) / self.actual_price) * 100
        return None

    def __repr__(self):
        return f'<Prediction {self.stock.symbol if self.stock else "N/A"} - {self.prediction_date}>'
