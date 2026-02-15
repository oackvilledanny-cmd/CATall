from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, HTTPException
import pandas as pd
from app.core.config import settings
from app.models.schemas import (
    BacktestRequest,
    BacktestResponse,
    IndicatorSnapshot,
    NewsResponse,
    PortfolioWeight,
    PortfolioWeightsRequest,
    PortfolioWeightsResponse,
    ScanCandidate,
    ScanResponse,
)
from app.providers.news_provider import MockNewsProvider
from app.providers.price_provider import YFinancePriceProvider
from app.services.backtest import run_backtest
from app.services.indicators import compute_indicators
from app.services.portfolio import compute_weights, realized_vol, take_profit_stop
from app.services.scoring import bullish_score

router = APIRouter(prefix="/api")
price_provider = YFinancePriceProvider()
news_provider = MockNewsProvider()


def _load_universe() -> list[str]:
    with open(settings.default_symbols_file, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def _disclaimer(payload: dict) -> dict:
    payload["disclaimer"] = settings.not_financial_advice
    return payload


@router.get("/scan", response_model=ScanResponse)
def scan(days: int = 60, threshold: float = 0.10, top_n: int = 50):
    out: list[ScanCandidate] = []
    universe = _load_universe()
    for ticker in universe:
        df = price_provider.get_daily_ohlcv(ticker, period="1y")
        if len(df) < max(days, 60):
            continue
        dfi = compute_indicators(df)
        dfi["vol20"] = dfi["volume"].rolling(20).mean()
        dfi["atr_pct"] = dfi["atr14"] / dfi["close"]
        recent = dfi.tail(days)
        jump_days = int((recent["ret"].abs() >= threshold).sum())
        last = dfi.iloc[-1].to_dict()
        prev = dfi.iloc[-2].to_dict()
        score, reasons = bullish_score(last, prev)
        out.append(
            ScanCandidate(
                ticker=ticker,
                jump_days=jump_days,
                score=score,
                reasons=reasons,
                indicators=IndicatorSnapshot(
                    ema20=last.get("ema20"), ema50=last.get("ema50"), rsi14=last.get("rsi14"),
                    macd=last.get("macd"), macd_signal=last.get("macd_signal"), macd_hist=last.get("macd_hist"),
                    bb_mid=last.get("bb_mid"), atr14=last.get("atr14"), adx14=last.get("adx14")
                )
            )
        )
    ranked = sorted(out, key=lambda x: (x.jump_days, x.score), reverse=True)
    payload = ScanResponse(
        disclaimer=settings.not_financial_advice,
        params={"days": days, "threshold": threshold, "top_n": top_n},
        universe_size=len(universe),
        candidates=ranked[:top_n],
        top10=sorted(ranked[:top_n], key=lambda x: x.score, reverse=True)[:10],
    )
    return payload


@router.get("/symbol/{ticker}/chart")
def chart(ticker: str):
    df = price_provider.get_daily_ohlcv(ticker, period="6mo")
    if df.empty:
        raise HTTPException(404, "ticker not found")
    dfi = compute_indicators(df)
    return _disclaimer({"ticker": ticker, "bars": dfi.fillna(0).to_dict("records")})


@router.get("/symbol/{ticker}/indicators")
def indicators(ticker: str):
    df = price_provider.get_daily_ohlcv(ticker, period="1y")
    if len(df) < 60:
        raise HTTPException(404, "insufficient data")
    dfi = compute_indicators(df)
    dfi["vol20"] = dfi["volume"].rolling(20).mean()
    dfi["atr_pct"] = dfi["atr14"] / dfi["close"]
    score, reasons = bullish_score(dfi.iloc[-1].to_dict(), dfi.iloc[-2].to_dict())
    return _disclaimer({"ticker": ticker, "score": score, "reasons": reasons, "latest": dfi.iloc[-1].fillna(0).to_dict()})


@router.get("/symbol/{ticker}/news", response_model=NewsResponse)
def news(ticker: str, days: int = 14):
    items = news_provider.get_recent_news(ticker, days=days)
    return NewsResponse(disclaimer=settings.not_financial_advice, ticker=ticker, items=items)


@router.post("/portfolio/weights", response_model=PortfolioWeightsResponse)
def portfolio_weights(req: PortfolioWeightsRequest):
    tickers = req.tickers[: req.risk_profile.max_positions]
    vol_map: dict[str, float] = {}
    score_map: dict[str, int] = {}
    output: list[PortfolioWeight] = []
    for ticker in tickers:
        df = price_provider.get_daily_ohlcv(ticker, period="6mo")
        if df.empty:
            continue
        dfi = compute_indicators(df)
        dfi["vol20"] = dfi["volume"].rolling(20).mean()
        dfi["atr_pct"] = dfi["atr14"] / dfi["close"]
        vol_map[ticker] = max(realized_vol(dfi["ret"]), 1e-6)
        score_map[ticker], _ = bullish_score(dfi.iloc[-1].to_dict(), dfi.iloc[-2].to_dict())

    weights = compute_weights(vol_map, req.method, score_map, req.risk_profile.max_weight_per_asset)
    for ticker, weight in weights.items():
        df = compute_indicators(price_provider.get_daily_ohlcv(ticker, period="6mo"))
        last = df.iloc[-1]
        take, stop = take_profit_stop(last["close"], float(last.get("atr14", 0)))
        output.append(PortfolioWeight(ticker=ticker, weight=weight, expected_volatility=vol_map[ticker], take_profit=take, stop_loss=stop))

    return PortfolioWeightsResponse(
        disclaimer=settings.not_financial_advice,
        weights=output,
        notes="Weights respect user risk profile caps. Sell levels are example ATR-based rules and should be tuned."
    )


@router.post("/backtest", response_model=BacktestResponse)
def backtest(req: BacktestRequest):
    period = f"{req.lookback_years}y"
    df = price_provider.get_daily_ohlcv(req.ticker, period=period)
    if df.empty:
        raise HTTPException(404, "ticker not found")
    result = run_backtest(compute_indicators(df), req.fee_bps, req.slippage_bps)
    # Firestore persistence point (omitted concrete client wiring in MVP)
    return BacktestResponse(disclaimer=settings.not_financial_advice, ticker=req.ticker, **result)


@router.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat(), "disclaimer": settings.not_financial_advice}
