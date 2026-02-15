from __future__ import annotations
import numpy as np
import pandas as pd


def compute_weights(vol_map: dict[str, float], method: str, scores: dict[str, int], max_weight: float) -> dict[str, float]:
    tickers = list(vol_map.keys())
    if not tickers:
        return {}
    if method == "equal_weight":
        raw = np.array([1.0] * len(tickers))
    elif method == "score_weight":
        raw = np.array([max(scores.get(t, 1), 1) for t in tickers], dtype=float)
    else:
        raw = np.array([1.0 / max(vol_map[t], 1e-6) for t in tickers], dtype=float)

    w = raw / raw.sum()
    w = np.minimum(w, max_weight)
    if w.sum() == 0:
        w = np.array([1 / len(tickers)] * len(tickers))
    else:
        w /= w.sum()
    return {t: float(v) for t, v in zip(tickers, w)}


def take_profit_stop(last_close: float, atr: float, m: float = 1.5, n: float = 3.0) -> tuple[float, float]:
    stop = max(0.0, last_close - atr * m)
    take = last_close + atr * n
    return take, stop


def realized_vol(ret_series: pd.Series, annualization: int = 252) -> float:
    if ret_series.empty:
        return 0.0
    return float(ret_series.std() * np.sqrt(annualization))
