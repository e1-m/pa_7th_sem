from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='src/.env', env_file_encoding='utf-8')

    ACCESS_TOKEN_EXPIRATION_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 15
    ALGORITHM: str = "HS256"

    CORS_ORIGINS: list[str] = ["*"]

    SAME_SITE_COOKIE: Literal['strict', 'lax', 'none'] = "strict"

    TOKEN_SECRET_KEY: str

    POSTGRESQL_DB_URL: str


settings = Settings()
