from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    DEBUG: bool
    DATABASE_URL: str
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
