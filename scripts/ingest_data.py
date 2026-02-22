#!/usr/bin/env python
"""
Data Ingestion Script

Fetches data from FRED API and calculates Global Liquidity Index.
Can be run manually or via cron job for automated updates.

Usage:
    python scripts/ingest_data.py
    python scripts/ingest_data.py --days 90  # Fetch last 90 days
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import SessionLocal
from app.services.data_ingestion_service import DataIngestionService


async def main(days_back: int = 365):
    """
    Main function to ingest data and calculate GLI

    Args:
        days_back: Number of days of historical data to fetch
    """
    print("=" * 60)
    print("Global Liquidity Tracker - Data Ingestion")
    print("=" * 60)
    print()

    db = SessionLocal()

    try:
        service = DataIngestionService(db)

        # Ingest Fed data
        print("📥 Step 1: Fetching Federal Reserve data from FRED...")
        fed_results = await service.ingest_fed_data(days_back=days_back)
        print(f"✅ {fed_results['status']}: {fed_results['records_added']} records added")
        print(f"   Date range: {fed_results['date_range']}")
        print()

        # Calculate GLI
        print("🧮 Step 2: Calculating Global Liquidity Index...")
        gli_results = await service.calculate_and_store_gli()
        print(f"✅ {gli_results['status']}: {gli_results['gli_records_added']} GLI records calculated")
        print()

        # Summary
        print("=" * 60)
        print("✨ Data ingestion completed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  - Start the API server: python main.py")
        print("  - View data at: http://localhost:8000/api/v1/gli/current")
        print()

    except Exception as e:
        print(f"❌ Error during data ingestion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest data from FRED and calculate GLI")
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="Number of days of historical data to fetch (default: 365)"
    )

    args = parser.parse_args()

    asyncio.run(main(days_back=args.days))
