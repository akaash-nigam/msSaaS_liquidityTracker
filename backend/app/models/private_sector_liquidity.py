from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database import Base


class PrivateSectorLiquidity(Base):
    __tablename__ = "private_sector_liquidity"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    series_id = Column(String(50), nullable=False, index=True)
    value = Column(Numeric(20, 4), nullable=False)  # in billions USD
    unit = Column(String(50), default="billions_usd")
    frequency = Column(String(20))
    category = Column(String(50))  # shadow_banking, traditional_banking, corporate_debt
    subcategory = Column(String(50))
    data_source = Column(String(50), default="FRED")
    created_at = Column(DateTime, server_default=func.now())


class PrivateSectorLiquidityIndex(Base):
    __tablename__ = "private_sector_liquidity_index"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    total_value = Column(Numeric(20, 4), nullable=False)  # TPSL in trillions USD
    m2_value = Column(Numeric(20, 4))
    mmf_value = Column(Numeric(20, 4))
    commercial_paper_value = Column(Numeric(20, 4))
    repos_net_value = Column(Numeric(20, 4))
    bank_credit_value = Column(Numeric(20, 4))
    change_pct = Column(Numeric(10, 4))
    change_1m_pct = Column(Numeric(10, 4))
    data_quality = Column(String(20), default="partial")  # partial, full
    num_components = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


class EnhancedGlobalLiquidityIndex(Base):
    __tablename__ = "enhanced_global_liquidity_index"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    total_value = Column(Numeric(20, 4), nullable=False)  # Enhanced GLI in trillions USD
    central_bank_liquidity = Column(Numeric(20, 4))
    private_sector_liquidity = Column(Numeric(20, 4))
    cb_percentage = Column(Numeric(10, 4))
    ps_percentage = Column(Numeric(10, 4))
    change_pct = Column(Numeric(10, 4))
    change_1m_pct = Column(Numeric(10, 4))
    created_at = Column(DateTime, server_default=func.now())
