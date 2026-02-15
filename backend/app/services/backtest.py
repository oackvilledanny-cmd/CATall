from __future__ import annotations
import pandas as pd


def run_backtest(df: pd.DataFrame, fee_bps: float = 10.0, slippage_bps: float = 10.0) -> dict:
    fee = (fee_bps + slippage_bps) / 10000.0
    pos = 0
    entry = 0.0
    equity = 1.0
    peak = 1.0
    wins = 0
    trades = 0
    trade_rets = []
    curve = []

    for _, row in df.iterrows():
        buy = row.get("ema20", 0) > row.get("ema50", 0) and row.get("macd_hist", -1) > 0 and row.get("rsi14", 100) < 70
        sell = row.get("close", 0) < row.get("ema20", 0) or row.get("rsi14", 0) > 75
        if pos == 0 and buy:
            pos = 1
            entry = row["close"] * (1 + fee)
            trades += 1
        elif pos == 1 and sell:
            exit_px = row["close"] * (1 - fee)
            r = (exit_px - entry) / entry
            equity *= (1 + r)
            trade_rets.append(r)
            wins += int(r > 0)
            pos = 0
        peak = max(peak, equity)
        curve.append({"date": str(row["date"]), "equity": equity})

    if pos == 1:
        exit_px = df.iloc[-1]["close"] * (1 - fee)
        r = (exit_px - entry) / entry
        equity *= (1 + r)
        trade_rets.append(r)
        wins += int(r > 0)

    years = max(len(df) / 252, 1e-6)
    cagr = (equity ** (1 / years)) - 1
    dd = min([c["equity"] for c in curve]) / max([c["equity"] for c in curve]) - 1 if curve else 0
    return {
        "cagr": float(cagr),
        "max_drawdown": float(dd),
        "win_rate": float(wins / max(len(trade_rets), 1)),
        "avg_trade_return": float(sum(trade_rets) / max(len(trade_rets), 1)),
        "trades": int(max(trades, len(trade_rets))),
        "equity_curve": curve,
    }
