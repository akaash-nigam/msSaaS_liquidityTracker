"""
Liquidity Valuation Data Ingestion Script (Phase 5)
Fetches Buffett Indicator (Market Cap / GDP) for 10 countries from FRED
"""

import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta, datetime
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import SessionLocal, Base, engine
from app.services.fred_service import FREDService
from app.models.liquidity_valuation import LiquidityValuation

# GDP estimates in trillions USD (for computing market_cap_usd)
GDP_ESTIMATES = {
    "USA": 28.3, "JPA": 4.2, "CNA": 17.9, "GBA": 3.3, "DEA": 4.5,
    "FRA": 3.0, "CAA": 2.1, "INA": 3.7, "KRA": 1.7, "BRA": 2.0,
}


async def main():
    print("\n" + "=" * 80)
    print("LIQUIDITY VALUATION DATA INGESTION - PHASE 5")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Create table if not exists
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    fred = FREDService()

    end_date = date.today()
    start_date = end_date - timedelta(days=365 * 30)  # 30 years

    total_stored = 0

    try:
        for country_code, config in fred.BUFFETT_INDICATOR_SERIES.items():
            print(f"\nFetching {config['name']} ({config['series_id']})...")
            try:
                data = await fred.fetch_series(config["series_id"], start_date, end_date)
                observations = data.get("observations", [])
                print(f"  Retrieved {len(observations)} data points")

                count = 0
                gdp_est = GDP_ESTIMATES.get(country_code, 1.0)
                for obs in observations:
                    existing = db.query(LiquidityValuation).filter(
                        LiquidityValuation.country_code == country_code,
                        LiquidityValuation.date == obs["date"],
                    ).first()
                    if not existing:
                        ratio = Decimal(str(obs["value"]))
                        db.add(LiquidityValuation(
                            date=obs["date"],
                            country_code=country_code,
                            country_name=config["name"],
                            market_cap_to_gdp=ratio,
                            gdp_usd=Decimal(str(gdp_est)),
                            market_cap_usd=Decimal(str(gdp_est)) * ratio / 100,
                            series_id=config["series_id"],
                            data_source="FRED_WORLDBANK",
                        ))
                        count += 1

                db.commit()
                print(f"  Stored {count} new records")
                total_stored += count

            except Exception as e:
                print(f"  Error: {e}")
                db.rollback()

        print("\n" + "=" * 80)
        print("VALUATION INGESTION COMPLETE")
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
