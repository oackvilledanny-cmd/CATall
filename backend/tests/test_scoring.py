from app.services.scoring import bullish_score


def test_bullish_score_range():
    prev = {"rsi14": 50, "macd_hist": -0.1, "close": 10, "bb_mid": 10}
    last = {"ema20": 12, "ema50": 10, "rsi14": 55, "macd_hist": 0.2, "close": 11, "bb_mid": 10.5, "volume": 2000, "vol20": 1000, "atr_pct": 0.05}
    score, reasons = bullish_score(last, prev)
    assert 0 <= score <= 100
    assert len(reasons) >= 1
