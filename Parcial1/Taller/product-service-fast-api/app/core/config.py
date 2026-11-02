from sqlalchemy import URL
from pydantic_settings import BaseSettings, SettingsConfigDict

#
# from pydantic_settings import (
# BaseSettings,
# SettingsConfigDict,
# )


class Settings(BaseSettings):

    APP_NAME: str = "product-service"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    ENABLE_SEED: bool = False

    # ==========================================
    # PostgreSQL
    # ==========================================

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # ==========================================
    # User Service
    # ==========================================

    USER_SERVICE_URL: str = "http://127.0.0.1:3001"

    USER_SERVICE_AUTH_ME_PATH: str = "/api/v1/auth/me"

    USER_SERVICE_TIMEOUT_SECONDS: float = 3.0

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    @property
    def DATABASE_URL(self) -> URL:
        return URL.create("postgresql+psycopg", username=self.DB_USER,
            password=self.DB_PASSWORD, host=self.DB_HOST, port=self.DB_PORT,
            database=self.DB_NAME)


settings = Settings()
