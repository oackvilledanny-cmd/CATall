import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.api import routes


def fake_df(days=260):
    return pd.DataFrame(
        {
            "date": pd.date_range("2023-01-01", periods=days),
            "open": [10 + i * 0.02 for i in range(days)],
            "high": [10.5 + i * 0.02 for i in range(days)],
            "low": [9.5 + i * 0.02 for i in range(days)],
            "close": [10 + i * 0.02 for i in range(days)],
            "volume": [100000 + i * 100 for i in range(days)],
        }
    )


class FakeProvider:
    def get_daily_ohlcv(self, ticker: str, period: str = "1y"):
        return fake_df(300 if period.endswith("y") else 130)


def test_api_flow(monkeypatch):
    monkeypatch.setattr(routes, "price_provider", FakeProvider())
    monkeypatch.setattr(routes, "_load_universe", lambda: ["SHOP.TO", "ENB.TO"])
    client = TestClient(app)

    s = client.get("/api/scan")
    assert s.status_code == 200
    assert "disclaimer" in s.json()

    c = client.get("/api/symbol/SHOP.TO/chart")
    assert c.status_code == 200

    i = client.get("/api/symbol/SHOP.TO/indicators")
    assert i.status_code == 200

    n = client.get("/api/symbol/SHOP.TO/news")
    assert n.status_code == 200

    p = client.post(
        "/api/portfolio/weights",
        json={
            "tickers": ["SHOP.TO", "ENB.TO"],
            "method": "risk_parity",
            "risk_profile": {"level": "balanced", "max_positions": 2, "max_weight_per_asset": 0.7, "max_drawdown_limit": 0.2},
        },
    )
    assert p.status_code == 200

    b = client.post("/api/backtest", json={"ticker": "SHOP.TO", "lookback_years": 2, "fee_bps": 10, "slippage_bps": 10})
    assert b.status_code == 200
