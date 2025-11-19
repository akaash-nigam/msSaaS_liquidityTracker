"""
Create database tables for private sector liquidity models
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine
from app.config import settings
from app.database import Base
from app.models.private_sector_liquidity import (
    PrivateSectorLiquidity,
    PrivateSectorLiquidityIndex,
    EnhancedGlobalLiquidityIndex
)


def create_tables():
    """Create all private sector liquidity tables"""

    # Create engine
    engine = create_engine(settings.DATABASE_URL)

    print("🗄️  Creating private sector liquidity tables...")

    # Create tables
    Base.metadata.create_all(bind=engine, tables=[
        PrivateSectorLiquidity.__table__,
        PrivateSectorLiquidityIndex.__table__,
        EnhancedGlobalLiquidityIndex.__table__
    ])

    print("✅ Tables created successfully!")
    print(f"   - {PrivateSectorLiquidity.__tablename__}")
    print(f"   - {PrivateSectorLiquidityIndex.__tablename__}")
    print(f"   - {EnhancedGlobalLiquidityIndex.__tablename__}")


if __name__ == "__main__":
    create_tables()
