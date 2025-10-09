from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class GlobalLiquidityIndex(Base):
    """Model for calculated Global Liquidity Index"""
    __tablename__ = "global_liquidity_index"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    value = Column(Numeric(15, 2), nullable=False)  # GLI in trillions USD
    change_pct = Column(Numeric(8, 4))  # % change from previous
    change_1m_pct = Column(Numeric(8, 4))
    change_3m_pct = Column(Numeric(8, 4))
    change_6m_pct = Column(Numeric(8, 4))
    change_1y_pct = Column(Numeric(8, 4))
    cycle_position = Column(String(20))  # 'expansion', 'peak', 'contraction', 'trough'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_date_desc', date.desc()),
    )

    def __repr__(self):
        return f"<GlobalLiquidityIndex(date={self.date}, value={self.value})>"
