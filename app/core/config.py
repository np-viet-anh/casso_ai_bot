import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    telegram_token: str
    openai_api_key: str | None = None
    payos_client_id: str
    payos_api_key: str
    payos_checksum_key: str
    database_url: str = "sqlite:///./orders.db"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
