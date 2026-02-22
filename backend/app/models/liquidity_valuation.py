from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database import Base


class LiquidityValuation(Base):
    __tablename__ = "liquidity_valuations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    country_code = Column(String(5), nullable=False, index=True)
    country_name = Column(String(100), nullable=False)
    market_cap_to_gdp = Column(Numeric(10, 4))
    gdp_usd = Column(Numeric(20, 4))
    market_cap_usd = Column(Numeric(20, 4))
    series_id = Column(String(50))
    data_source = Column(String(50), default="FRED_WORLDBANK")
    created_at = Column(DateTime, server_default=func.now())
