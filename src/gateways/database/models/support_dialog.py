from datetime import date, datetime

from src.enums import SupportDialogStatusEnum
from src.gateways.database.database import Base
from sqlalchemy import Column, SmallInteger, func, DateTime, BigInteger, Date



class SupportDialog(Base):
    id: int = Column(BigInteger, primary_key=True)
    daily_dialog_count: int = Column(SmallInteger)
    dialog_date: date = Column(Date, index=True)
    user_id: int = Column(BigInteger, index=True)
    status: SupportDialogStatusEnum = Column(SmallInteger, default=SupportDialogStatusEnum.started)
    create_date: datetime = Column(DateTime, onupdate=func.now(), default=func.now(), nullable=False)
    update_date: datetime = Column(DateTime, onupdate=func.now(), default=func.now(), nullable=False)