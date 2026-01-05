"""
アプリケーション設定
環境変数から設定を読み込む
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """環境変数ベースの設定"""

    # アプリケーション基本設定
    APP_NAME: str = "Financial Intelligence System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # データベース設定
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/fin_intel"

    # AI API設定
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # データ収集API設定
    TWITTER_BEARER_TOKEN: str = ""
    FMP_API_KEY: str = ""  # Financial Modeling Prep
    ALPHA_VANTAGE_API_KEY: str = ""

    # 通知設定
    LINE_CHANNEL_ACCESS_TOKEN: str = ""
    SENDGRID_API_KEY: str = ""

    # Redis設定
    REDIS_URL: str = "redis://localhost:6379"

    # CORS設定
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """設定のシングルトンインスタンスを取得"""
    return Settings()
