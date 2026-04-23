from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "HealthAI - 智能情绪管理平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database - 使用SQLite便于本地测试
    DATABASE_URL: str = "sqlite:///./healthai.db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # API
    API_V1_PREFIX: str = "/api/v1"

    # PMS Risk Threshold
    PMS_RISK_HIGH_THRESHOLD: float = 0.7
    PMS_RISK_CRITICAL_THRESHOLD: float = 0.8

    # Cycle Prediction
    CYCLE_PREDICTION_MIN_HISTORY: int = 2  # Minimum cycles needed for prediction
    CYCLE_PREDICTION_ERROR_RANGE: int = 2  # Days

    # AI/ML (placeholder for actual services)
    NLP_CONFIDENCE_THRESHOLD: float = 0.6
    CONTEXT_WINDOW_SIZE: int = 10  # conversation turns

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
