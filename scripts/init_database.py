#!/usr/bin/env python
"""
Database Initialization Script

Creates all database tables and optionally seeds with sample data.

Usage:
    python scripts/init_database.py
    python scripts/init_database.py --drop  # Drop existing tables first
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import engine, Base, init_db
from app.models import CentralBankData, GlobalLiquidityIndex


def drop_tables():
    """Drop all tables"""
    print("🗑️  Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped")


def create_tables():
    """Create all tables"""
    print("📊 Creating database tables...")
    init_db()
    print("✅ Tables created successfully")


def main(drop_first: bool = False):
    """
    Initialize database

    Args:
        drop_first: If True, drop existing tables before creating new ones
    """
    print("=" * 60)
    print("Global Liquidity Tracker - Database Initialization")
    print("=" * 60)
    print()

    try:
        if drop_first:
            drop_tables()
            print()

        create_tables()
        print()

        print("=" * 60)
        print("✨ Database initialization completed!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Configure your .env file with FRED API key")
        print("  2. Run data ingestion: python scripts/ingest_data.py")
        print("  3. Start the API server: python main.py")
        print()

    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Initialize database for Global Liquidity Tracker")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop existing tables before creating new ones"
    )

    args = parser.parse_args()

    main(drop_first=args.drop)
