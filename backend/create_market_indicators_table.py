"""
Create market_indicators table in database
"""

from app.database import engine, Base
from app.models.market_indicators import MarketIndicator

def create_tables():
    """Create all tables defined in the models"""
    print("Creating market_indicators table...")
    Base.metadata.create_all(bind=engine)
    print("✅ Table created successfully!")

if __name__ == "__main__":
    create_tables()
