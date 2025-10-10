from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):
    admin_chat_id: int
    token: SecretStr
    webhook: AnyHttpUrl = "https://bbae6hvom2ckgp3f1fob.containers.yandexcloud.net"
