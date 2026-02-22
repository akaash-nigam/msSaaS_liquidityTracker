from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database import Base


class MarketIndicator(Base):
    __tablename__ = "market_indicators"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    indicator_name = Column(String(100), nullable=False)
    series_id = Column(String(50))
    value = Column(Numeric(20, 4), nullable=False)
    unit = Column(String(50))
    category = Column(String(50))  # yield_curve, credit_spread, volatility, etc.
    data_source = Column(String(50), default="FRED")
    created_at = Column(DateTime, server_default=func.now())
