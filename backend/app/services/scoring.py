from __future__ import annotations
import math

WEIGHTS = {
    "trend": 20,
    "rsi": 15,
    "macd": 15,
    "bb_mid": 10,
    "volume": 10,
    "atr_penalty": -10,
}


def bullish_score(last: dict, prev: dict) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    if last.get("ema20", 0) > last.get("ema50", math.inf):
        score += WEIGHTS["trend"]
        reasons.append("EMA20 > EMA50 uptrend")
    if 45 <= last.get("rsi14", 0) <= 65 and last.get("rsi14", 0) > prev.get("rsi14", 0):
        score += WEIGHTS["rsi"]
        reasons.append("RSI in bullish-neutral zone and rising")
    if prev.get("macd_hist", -1) <= 0 < last.get("macd_hist", -1):
        score += WEIGHTS["macd"]
        reasons.append("MACD histogram crossed above zero")
    if prev.get("close", 0) <= prev.get("bb_mid", 0) and last.get("close", 0) > last.get("bb_mid", 0):
        score += WEIGHTS["bb_mid"]
        reasons.append("Close crossed above Bollinger mid-band")
    if last.get("volume", 0) >= 1.5 * last.get("vol20", 1):
        score += WEIGHTS["volume"]
        reasons.append("Volume surge >= 1.5x 20D average")
    if last.get("atr_pct", 0) > 0.12:
        score += WEIGHTS["atr_penalty"]
        reasons.append("ATR volatility overheat penalty")
    return max(0, min(100, score)), reasons
