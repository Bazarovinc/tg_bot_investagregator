from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, func,DateTime, Numeric

from src.gateways.database.database import Base


class Product(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    profitability: Decimal = Column(Numeric(5, 2), nullable=True)
    agent_profitability: Decimal = Column(Numeric(5, 2), nullable=True)
    placement_period: int = Column(SmallInteger, nullable=True)
    profitability_readable: str = Column(String)
    agent_profitability_readable: str = Column(String)
    placement_period_readable: str = Column(String)
    product_type_id: int = Column(
        ForeignKey("product_type.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: str = Column(String)
    file_path: str = Column(String)
    create_date: datetime = Column(DateTime, onupdate=func.now(), default=func.now(), nullable=False)
    update_date: datetime = Column(DateTime, onupdate=func.now(), default=func.now(), nullable=False)
