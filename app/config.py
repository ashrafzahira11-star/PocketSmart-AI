from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "change-this-secret"

    database_url: str = "sqlite:///./pocketsmart.db"

    gemini_api_key: str = ""

    gemini_model: str = "gemini-3.8-flash"

    use_gemini: bool = True

    access_token_expire_minutes: int = 120

    max_upload_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()