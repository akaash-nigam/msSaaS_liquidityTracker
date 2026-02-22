from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database import Base


class CentralBankData(Base):
    __tablename__ = "central_bank_data"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(10), nullable=False, index=True)  # FED, ECB, BOJ, etc.
    indicator = Column(String(50), nullable=False)  # balance_sheet, etc.
    value = Column(Numeric(20, 4), nullable=False)  # in trillions
    currency = Column(String(5), nullable=False, default="USD")
    date = Column(Date, nullable=False, index=True)
    series_id = Column(String(50))
    data_source = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class GlobalLiquidityIndex(Base):
    __tablename__ = "global_liquidity_index"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    value = Column(Numeric(20, 4), nullable=False)  # in trillions USD
    change_pct = Column(Numeric(10, 4))  # daily change %
    change_1m_pct = Column(Numeric(10, 4))  # 1-month change %
    num_sources = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    from_currency = Column(String(5), nullable=False, index=True)
    to_currency = Column(String(5), nullable=False, default="USD")
    date = Column(Date, nullable=False, index=True)
    rate = Column(Numeric(20, 10), nullable=False)
    series_id = Column(String(50))
    data_source = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
