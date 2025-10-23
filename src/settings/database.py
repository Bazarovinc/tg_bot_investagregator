from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    scheme: Literal["postgresql+asyncpg", "postgresql"] = "postgresql+asyncpg"
    host: str = "localhost"
    port: str = "15432"
    user: str = "postgres"
    password: SecretStr
    db: str = "tg_bot"
    pool_size: int = 10
    pool_overflow_size: int = 15
    pool_pre_ping: bool = True
    echo: bool = False
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False
    local: bool = False

    @property
    def dsn(self) -> str:
        """
        Формирует строку подключения (DSN) к PostgreSQL

        Returns:
            строка подключения в формате: 'scheme://user:password@host:port/db'
        """
        return f"{self.scheme}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
