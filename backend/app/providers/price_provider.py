from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
import yfinance as yf


class PriceProvider(ABC):
    @abstractmethod
    def get_daily_ohlcv(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        ...


class YFinancePriceProvider(PriceProvider):
    def get_daily_ohlcv(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        df = yf.download(ticker, period=period, interval="1d", auto_adjust=False, progress=False)
        if df.empty:
            return df
        df = df.rename(columns=str.lower).reset_index().rename(columns={"Date": "date", "Datetime": "date"})
        if "date" not in df.columns:
            df = df.rename(columns={df.columns[0]: "date"})
        return df[["date", "open", "high", "low", "close", "volume"]].copy()
