from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings.database import DatabaseSettings


def get_session_maker(database_settings: DatabaseSettings) -> async_sessionmaker:
    return async_sessionmaker(
        autocommit=database_settings.autocommit,
        autoflush=database_settings.autoflush,
        class_=AsyncSession,
        bind=create_async_engine(
            database_settings.dsn,
            pool_pre_ping=database_settings.pool_pre_ping,
            echo=database_settings.echo,
            pool_size=database_settings.pool_size,
            max_overflow=database_settings.pool_overflow_size,
        ),
    )
