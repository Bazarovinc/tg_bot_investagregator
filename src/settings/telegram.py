from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):
    master_id: int = 457127990
    guard_chanel_id: str
    admin_chat_id: int
    support_chat_id: int
    token: SecretStr
    # webhook: AnyHttpUrl
