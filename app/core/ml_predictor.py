# Prediction service
# app/core/ml_predictor.py
import pandas as pd
from .ml_pipeline import MLPipeline

class MLPredictor:
    """Predicts stock price direction using trained ML model."""

    def __init__(self):
        self.pipeline = MLPipeline()
        self.trained = False

    def train_model(self, df: pd.DataFrame):
        acc = self.pipeline.train(df)
        self.trained = True
        return acc

    def predict_next(self, latest_data: pd.DataFrame) -> str:
        if not self.trained:
            raise ValueError("Model not trained yet.")
        pred = self.pipeline.predict(latest_data)
        return "UP" if pred == 1 else "DOWN"
