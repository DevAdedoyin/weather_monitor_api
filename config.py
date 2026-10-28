from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    database_url: str

    secret_key: SecretStr
    algorithm: str = "HS256"

    openai_api_key: str | None = None
    google_api_key: str | None = None
    deepseek_api_key: str | None = None
    openrouter_api_key: str | None = None
    open_weather_api_key: str | None = None
    google_cloud_key: str | None = None
    google_cloud_key_ios: str | None = None


settings = Settings()  # type: ignore[call-arg] # Loaded from .env file