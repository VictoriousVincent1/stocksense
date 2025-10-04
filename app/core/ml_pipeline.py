# ML training/prediction
# app/core/ml_pipeline.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class MLPipeline:
    """Pipeline for training ML models on stock data."""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def prepare_data(self, df: pd.DataFrame):
        df["Return"] = df["Close"].pct_change()
        df["Target"] = (df["Return"].shift(-1) > 0).astype(int)  # 1 = up, 0 = down
        df = df.dropna()

        X = df[["Open", "High", "Low", "Close", "Volume"]]
        y = df["Target"]

        return train_test_split(X, y, test_size=0.2, shuffle=False)

    def train(self, df: pd.DataFrame):
        X_train, X_test, y_train, y_test = self.prepare_data(df)
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        return accuracy_score(y_test, preds)

    def predict(self, latest_data: pd.DataFrame) -> int:
        return self.model.predict(latest_data)[0]
