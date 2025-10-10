from typing import Literal

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    scheme: Literal["sqlite+aiosqlite", "sqlite"] = "sqlite+aiosqlite"
    database_name: str = "database.db"

    pool_size: int = 10
    pool_overflow_size: int = 15
    pool_pre_ping: bool = True
    echo: bool = False
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False

    @property
    def dsn(self) -> str:
        return f"{self.scheme}:///{self.database_name}"
