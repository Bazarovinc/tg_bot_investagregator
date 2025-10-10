from dependency_injector import containers, providers

from src.gateways.database.session import get_session_maker
from src.gateways.object_storage_client import ObjectStorageClient
from src.settings.database import DatabaseSettings
from src.settings.object_storage import ObjectStorageSettings


class AppContainer(containers.DeclarativeContainer):
    db_config = DatabaseSettings()
    object_storage_config = ObjectStorageSettings()
    wiring_config = containers.WiringConfiguration(packages=["src.controllers.telegram_bot"])
    session_maker = providers.Factory(get_session_maker, database_settings=db_config)
    object_storage = providers.Singleton(ObjectStorageClient, settings=object_storage_config)
