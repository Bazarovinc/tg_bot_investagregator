from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, func
from sqlalchemy.dialects.sqlite import DATETIME

from src.gateways.database.database import Base


class Product(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    profitability: Decimal = Column(Integer, nullable=False)
    agent_profitability: Decimal = Column(Integer, nullable=False)
    placement_period: int = Column(SmallInteger, nullable=False)
    product_type_id: int = Column(
        ForeignKey("product_type.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: str = Column(String)
    file_path: str = Column(String)
    create_date: datetime = Column(DATETIME, onupdate=func.now(), default=func.now(), nullable=False)
    update_date: datetime = Column(DATETIME, onupdate=func.now(), default=func.now(), nullable=False)
