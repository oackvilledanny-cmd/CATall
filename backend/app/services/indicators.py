from __future__ import annotations
import numpy as np
import pandas as pd


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema20"] = out["close"].ewm(span=20).mean()
    out["ema50"] = out["close"].ewm(span=50).mean()
    delta = out["close"].diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    rs = pd.Series(gain).rolling(14).mean() / (pd.Series(loss).rolling(14).mean() + 1e-9)
    out["rsi14"] = 100 - (100 / (1 + rs))
    ema12 = out["close"].ewm(span=12).mean()
    ema26 = out["close"].ewm(span=26).mean()
    out["macd"] = ema12 - ema26
    out["macd_signal"] = out["macd"].ewm(span=9).mean()
    out["macd_hist"] = out["macd"] - out["macd_signal"]
    out["bb_mid"] = out["close"].rolling(20).mean()
    std = out["close"].rolling(20).std()
    out["bb_upper"] = out["bb_mid"] + 2 * std
    out["bb_lower"] = out["bb_mid"] - 2 * std
    tr = np.maximum(out["high"] - out["low"], np.maximum(abs(out["high"] - out["close"].shift(1)), abs(out["low"] - out["close"].shift(1))))
    out["atr14"] = tr.rolling(14).mean()

    up_move = out["high"].diff()
    down_move = -out["low"].diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    tr14 = pd.Series(tr).rolling(14).sum() + 1e-9
    plus_di = 100 * (pd.Series(plus_dm).rolling(14).sum() / tr14)
    minus_di = 100 * (pd.Series(minus_dm).rolling(14).sum() / tr14)
    dx = 100 * abs((plus_di - minus_di) / (plus_di + minus_di + 1e-9))
    out["adx14"] = dx.rolling(14).mean()
    out["ret"] = out["close"].pct_change().fillna(0.0)
    out["abs_jump_10"] = (out["ret"].abs() >= 0.10).astype(int)
    return out
