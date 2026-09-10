from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    app_name: str = "FastAPI MCP Gateway"
    environment: str = Field(
        default="local",
        pattern=r"^(local|test|staging|production)$",
    )
    debug: bool = True
    api_prefix: str = "/api"
    mcp_endpoint_path: str = "/mcp"
    gateway_secret_key: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings()