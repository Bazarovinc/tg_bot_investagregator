from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):
    admin_chat_id: int
    token: SecretStr
    # webhook: AnyHttpUrl
