from pydantic import Field
from pydantic_settings import BaseSettings

from src.settings.database import DatabaseSettings
from src.settings.object_storage import ObjectStorageSettings
from src.settings.telegram import TelegramSettings


class AppSettings(BaseSettings):
    port: int = Field(default=8000)
    database: DatabaseSettings = DatabaseSettings()
    telegram: TelegramSettings = TelegramSettings()
    object_storage: ObjectStorageSettings = ObjectStorageSettings()


app_settings = AppSettings()
