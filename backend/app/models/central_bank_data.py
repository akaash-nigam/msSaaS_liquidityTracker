from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class CentralBankData(Base):
    """Model for central bank balance sheet data"""
    __tablename__ = "central_bank_data"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(10), nullable=False)  # 'FED', 'ECB', 'BOJ', etc.
    indicator = Column(String(50), nullable=False)  # 'balance_sheet', 'tga', 'rrp'
    date = Column(Date, nullable=False)
    value = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), nullable=False)  # 'USD', 'EUR', 'JPY'
    unit = Column(String(20))  # 'billions', 'trillions'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_source_indicator_date', 'source', 'indicator', 'date', unique=True),
        Index('idx_date', 'date'),
        Index('idx_source', 'source'),
    )

    def __repr__(self):
        return f"<CentralBankData(source={self.source}, date={self.date}, value={self.value})>"
