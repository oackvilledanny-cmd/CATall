from typing import Literal
from pydantic import BaseModel, Field


class IndicatorSnapshot(BaseModel):
    ema20: float | None = None
    ema50: float | None = None
    rsi14: float | None = None
    macd: float | None = None
    macd_signal: float | None = None
    macd_hist: float | None = None
    bb_mid: float | None = None
    atr14: float | None = None
    adx14: float | None = None


class ScanCandidate(BaseModel):
    ticker: str
    jump_days: int
    score: int
    reasons: list[str]
    indicators: IndicatorSnapshot


class ScanResponse(BaseModel):
    disclaimer: str
    params: dict
    universe_size: int
    candidates: list[ScanCandidate]
    top10: list[ScanCandidate]


class NewsItem(BaseModel):
    title: str
    source: str
    published_at: str
    url: str
    summary: str
    tag: Literal["positive", "negative", "uncertain"]


class NewsResponse(BaseModel):
    disclaimer: str
    ticker: str
    items: list[NewsItem]


class RiskProfile(BaseModel):
    level: Literal["conservative", "balanced", "aggressive"] = "balanced"
    max_positions: int = Field(default=5, ge=1, le=20)
    max_weight_per_asset: float = Field(default=0.25, ge=0.01, le=1.0)
    max_drawdown_limit: float = Field(default=0.2, ge=0.01, le=0.9)


class PortfolioWeightsRequest(BaseModel):
    tickers: list[str]
    method: Literal["risk_parity", "equal_weight", "score_weight"] = "risk_parity"
    risk_profile: RiskProfile


class PortfolioWeight(BaseModel):
    ticker: str
    weight: float
    expected_volatility: float
    take_profit: float
    stop_loss: float


class PortfolioWeightsResponse(BaseModel):
    disclaimer: str
    weights: list[PortfolioWeight]
    notes: str


class BacktestRequest(BaseModel):
    ticker: str
    lookback_years: int = Field(default=3, ge=1, le=10)
    fee_bps: float = Field(default=10.0, ge=0)
    slippage_bps: float = Field(default=10.0, ge=0)


class BacktestResponse(BaseModel):
    disclaimer: str
    ticker: str
    cagr: float
    max_drawdown: float
    win_rate: float
    avg_trade_return: float
    trades: int
    equity_curve: list[dict]
