from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from app.models.schemas import NewsItem


class NewsProvider(ABC):
    @abstractmethod
    def get_recent_news(self, ticker: str, days: int = 14) -> list[NewsItem]:
        ...


class MockNewsProvider(NewsProvider):
    def get_recent_news(self, ticker: str, days: int = 14) -> list[NewsItem]:
        now = datetime.utcnow()
        return [
            NewsItem(
                title=f"{ticker} posts quarterly update",
                source="MockWire",
                published_at=(now - timedelta(days=1)).isoformat(),
                url="https://example.com/news/1",
                summary="Earnings update with mixed guidance and stable cash position.",
                tag="uncertain",
            ),
            NewsItem(
                title=f"{ticker} secures strategic partnership",
                source="MockWire",
                published_at=(now - timedelta(days=3)).isoformat(),
                url="https://example.com/news/2",
                summary="Partnership may support medium-term demand growth.",
                tag="positive",
            ),
            NewsItem(
                title=f"Sector volatility affects {ticker}",
                source="MockWire",
                published_at=(now - timedelta(days=5)).isoformat(),
                url="https://example.com/news/3",
                summary="Macro uncertainty remains a downside risk for near-term prices.",
                tag="negative",
            ),
        ]
