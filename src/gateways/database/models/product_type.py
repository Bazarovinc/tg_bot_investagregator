from datetime import datetime

from sqlalchemy import Column, Integer, String, func
from sqlalchemy.dialects.sqlite import DATETIME

from src.gateways.database.database import Base


class ProductType(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True, nullable=False)
    create_date: datetime = Column(DATETIME, onupdate=func.now(), default=func.now(), nullable=False)
    update_date: datetime = Column(DATETIME, onupdate=func.now(), default=func.now(), nullable=False)
