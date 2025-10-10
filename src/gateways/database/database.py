from typing import Any, TypeVar

from sqlalchemy import MetaData, Table
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from src.utils import camel_to_snake


@as_declarative()
class Base:
    metadata: MetaData

    __table__: Table

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # Для корректной работы mypy
        pass

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return camel_to_snake(cls.__name__)

    __mapper_args__ = {"eager_defaults": True}


ModelType = TypeVar("ModelType", bound=Base)
