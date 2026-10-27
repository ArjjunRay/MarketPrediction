from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded exclusively from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="QSTREAM_",
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Literal["development", "test", "staging", "production"] = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    public_mode: bool = True
    enable_simulated_provider: bool = False
    database_url: str = "postgresql+asyncpg://qstream:change-me-local-only@localhost:55432/qstream"
    redis_url: str = "redis://localhost:6379/0"
    kafka_bootstrap_servers: str = "localhost:19092"
    schema_registry_url: str = "http://localhost:8081"
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    s3_endpoint: str = "http://localhost:59000"
    s3_access_key: str = "qstream"
    s3_secret_key: str = "change-me-local-only"
    s3_bucket: str = "qstream-local"
    s3_region: str = "us-east-1"
    sec_user_agent: str = ""
    bea_api_key: str = ""
    public_data_timeout_seconds: float = 30.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
