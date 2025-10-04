"""
StockSense AI - Pandas Quick Reference
PURPOSE: Copy these patterns into your actual code
"""

import pandas as pd
import numpy as np

# =============================================================================
# COPY-PASTE PATTERNS - Use these in your actual StockSense AI code
# =============================================================================

# PATTERN 1: Moving Averages (copy this wherever you have df)
# df['sma_20'] = df['Close'].rolling(20).mean()
# df['sma_50'] = df['Close'].rolling(50).mean()
# df['ema_12'] = df['Close'].ewm(span=12).mean()

# PATTERN 2: Returns (copy this wherever you have df)  
# df['daily_returns'] = df['Close'].pct_change()
# df['weekly_returns'] = df['Close'].pct_change(periods=7)

# PATTERN 3: Technical Indicators (copy this wherever you have df)
# df['rsi'] = calculate_rsi(df['Close'])  # You'll need the RSI function too

# PATTERN 4: Filtering (copy this wherever you have df)
# high_volume = df[df['Volume'] > df['Volume'].mean()]
# positive_days = df[df['Close'].pct_change() > 0]

# =============================================================================
# TEST FUNCTION - Shows patterns in action with real data
# =============================================================================

def test_patterns_with_real_data():
    """Test all patterns with real AAPL data"""
    import yfinance as yf
    
    # Get real data (this is how df gets defined)
    df = yf.download("AAPL", period="3mo")
    print(f"✅ Got {len(df)} days of AAPL data")
    
    # Apply patterns from above:
    df['sma_20'] = df['Close'].rolling(20).mean()
    df['daily_returns'] = df['Close'].pct_change()
    high_volume = df[df['Volume'] > df['Volume'].mean()]
    
    print(f"Latest price: ${df['Close'].iloc[-1]:.2f}")
    print(f"Latest SMA 20: ${df['sma_20'].iloc[-1]:.2f}")
    print(f"High volume days: {len(high_volume)}")
    
    return df

if __name__ == "__main__":
    test_patterns_with_real_data()