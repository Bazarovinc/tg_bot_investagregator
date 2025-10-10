from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class ObjectStorageSettings(BaseSettings):
    service_name: str = "s3"
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str = "ru-central1"
    endpoint_url: AnyHttpUrl = AnyHttpUrl("https://storage.yandexcloud.net")
    bucket_name: str = "agent-bot-files"
