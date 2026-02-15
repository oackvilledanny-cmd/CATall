from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CA Tall Scanner API"
    not_financial_advice: str = "Not financial advice. For informational and educational purposes only."
    price_provider: str = "yfinance"
    news_provider: str = "mock"
    firestore_project_id: str = ""
    default_symbols_file: str = "backend/app/core/tsx_symbols.txt"

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")


settings = Settings()
