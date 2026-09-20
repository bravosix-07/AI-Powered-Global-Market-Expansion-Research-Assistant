from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    AISA_API_KEY: str = ""
    AISA_BASE_URL: str = "https://api.aisa.one/v1"
    AISA_DATA_BASE_URL: str = "https://api.aisa.one/apis/v1"
    MODEL_NAME: str = "kimi-k2.6"


@lru_cache
def get_settings() -> Settings:
    return Settings()
