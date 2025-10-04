# Data validation/cleaning# app/core/data_cleaner.py
import pandas as pd

class DataCleaner:
    """Cleans and validates stock data."""

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna()
        df = df.drop_duplicates()
        df = df.sort_values("Date")
        return df.reset_index(drop=True)

    @staticmethod
    def validate(df: pd.DataFrame) -> bool:
        return not df.empty and all(col in df.columns for col in ["Date", "Open", "High", "Low", "Close", "Volume"])
