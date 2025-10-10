from io import BytesIO

from aioboto3 import Session

from src.settings.object_storage import ObjectStorageSettings


class ObjectStorageClient:
    def __init__(self, settings: ObjectStorageSettings) -> None:
        self.settings = settings
        self._session = Session(
            aws_access_key_id=self.settings.aws_access_key_id, aws_secret_access_key=self.settings.aws_secret_access_key
        )

    async def save_file(self, file: BytesIO, file_key: str) -> None:
        async with self._session.client(
            service_name=self.settings.service_name,
            endpoint_url=self.settings.endpoint_url.encoded_string(),
        ) as client:
            await client.put_object(Bucket=self.settings.bucket_name, Key=file_key, Body=file)

    async def get_file(self, file_key: str) -> BytesIO:
        async with self._session.client(
            service_name=self.settings.service_name, endpoint_url=self.settings.endpoint_url.encoded_string()
        ) as client:
            response = await client.get_object(Bucket=self.settings.bucket_name, Key=file_key)
            file_content = await response["Body"].read()
            return BytesIO(file_content)

    async def delete_file(self, file_key: str) -> None:
        async with self._session.client(
            service_name=self.settings.service_name, endpoint_url=self.settings.endpoint_url.encoded_string()
        ) as client:
            await client.delete_object(Bucket=self.settings.bucket_name, Key=file_key)
