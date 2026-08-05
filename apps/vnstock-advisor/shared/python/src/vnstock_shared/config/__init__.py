from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://vnstock:vnstock@localhost:5432/vnstock_advisor",
        description="PostgreSQL connection URL with asyncpg driver",
    )

    # Redis
    redis_url: str = Field(
        default="redis://:vnstock@localhost:6379/0",
        description="Redis connection URL",
    )

    # JWT
    jwt_private_key: str = Field(..., description="RSA private key for JWT signing")
    jwt_public_key: str = Field(..., description="RSA public key for JWT verification")
    jwt_algorithm: str = Field(default="RS256", description="JWT algorithm")
    jwt_access_token_expire_minutes: int = Field(default=30, description="Access token expiry")
    jwt_refresh_token_expire_days: int = Field(default=7, description="Refresh token expiry")

    # Data sources
    vnstock_api_key: Optional[str] = Field(default=None, description="Vnstock API key")
    alpha_vantage_api_key: Optional[str] = Field(default=None, description="Alpha Vantage API key")
    twelve_data_api_key: Optional[str] = Field(default=None, description="Twelve Data API key")

    # Service configs
    data_ingest_port: int = Field(default=8001, description="Data ingest service port")
    analysis_engine_port: int = Field(default=8002, description="Analysis engine service port")
    suggestion_api_port: int = Field(default=8003, description="Suggestion API service port")
    web_ui_port: int = Field(default=3000, description="Web UI port")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")


@lru_cache
def get_settings() -> Settings:
    return Settings()