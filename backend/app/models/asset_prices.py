from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database import Base


class AssetPrice(Base):
    __tablename__ = "asset_prices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    asset_name = Column(String(100), nullable=False, index=True)
    ticker = Column(String(20))
    price = Column(Numeric(20, 4), nullable=False)
    volume = Column(Numeric(20, 4))
    market_cap = Column(Numeric(20, 4))
    asset_class = Column(String(50))  # equity, crypto, commodity, bond
    data_source = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())


class AssetCorrelation(Base):
    __tablename__ = "asset_correlations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    asset_name = Column(String(100), nullable=False)
    correlation_30d = Column(Numeric(10, 6))
    correlation_90d = Column(Numeric(10, 6))
    correlation_365d = Column(Numeric(10, 6))
    beta_to_gli = Column(Numeric(10, 6))
    gli_value = Column(Numeric(20, 4))
    created_at = Column(DateTime, server_default=func.now())
