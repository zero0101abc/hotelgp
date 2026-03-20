from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database/hotelsys.db"
    SECRET_KEY: str = "supersecretkey123456789"
    SESSION_SECRET_KEY: str = "session-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SESSION_COOKIE_NAME: str = "hotelsys_session"
    SESSION_COOKIE_MAX_AGE: int = 60 * 60 * 24 * 90  # 90 days in seconds

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
