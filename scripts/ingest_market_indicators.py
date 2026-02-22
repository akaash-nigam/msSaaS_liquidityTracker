"""
Market Indicators Data Ingestion Script (Phase 4)
Fetches VIX, yield curve, credit spreads, and breakeven inflation from FRED
"""

import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta, datetime
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import SessionLocal
from app.services.fred_service import FREDService
from app.models.market_indicators import MarketIndicator


async def main():
    print("\n" + "=" * 80)
    print("MARKET INDICATORS DATA INGESTION - PHASE 4")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    db = SessionLocal()
    fred = FREDService()

    end_date = date.today()
    start_date = end_date - timedelta(days=365)

    total_stored = 0

    try:
        for series_id, config in fred.MARKET_INDICATOR_SERIES.items():
            print(f"\nFetching {config['name']} ({series_id})...")
            try:
                data = await fred.fetch_series(series_id, start_date, end_date)
                observations = data.get("observations", [])
                print(f"  Retrieved {len(observations)} data points")

                count = 0
                for obs in observations:
                    existing = db.query(MarketIndicator).filter(
                        MarketIndicator.series_id == series_id,
                        MarketIndicator.date == obs["date"],
                    ).first()
                    if not existing:
                        db.add(MarketIndicator(
                            date=obs["date"],
                            indicator_name=config["name"],
                            series_id=series_id,
                            value=Decimal(str(obs["value"])),
                            unit=config["unit"],
                            category=config["category"],
                            data_source="FRED",
                        ))
                        count += 1

                db.commit()
                print(f"  Stored {count} new records")
                total_stored += count

            except Exception as e:
                print(f"  Error: {e}")
                db.rollback()

        print("\n" + "=" * 80)
        print("MARKET INDICATORS INGESTION COMPLETE")
        print("=" * 80)
        print(f"Total Records Stored: {total_stored}")
        print("=" * 80)

    except Exception as e:
        print(f"\nError during ingestion: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
