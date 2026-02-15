import pandas as pd
from app.services.indicators import compute_indicators


def test_compute_indicators_has_columns():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=80),
            "open": [10 + i * 0.1 for i in range(80)],
            "high": [10.5 + i * 0.1 for i in range(80)],
            "low": [9.5 + i * 0.1 for i in range(80)],
            "close": [10 + i * 0.1 for i in range(80)],
            "volume": [1000 + i * 5 for i in range(80)],
        }
    )
    out = compute_indicators(df)
    for col in ["ema20", "ema50", "rsi14", "macd_hist", "atr14", "adx14", "ret"]:
        assert col in out.columns
