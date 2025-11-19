#!/usr/bin/env python3
"""
Script to ingest global central bank data and exchange rates
"""

import sys
import os
import asyncio

# Add parent directory to path to import from backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, engine, Base
from app.models import CentralBankData, GlobalLiquidityIndex, ExchangeRate
from app.services.data_ingestion_service import DataIngestionService


async def main():
    """Ingest global data from all central banks"""

    print("=" * 70)
    print("🌍 GLOBAL LIQUIDITY DATA INGESTION")
    print("=" * 70)
    print()

    # Create tables if they don't exist
    print("📋 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")
    print()

    # Create database session
    db = SessionLocal()

    try:
        # Create ingestion service
        service = DataIngestionService(db)

        # Ingest data (1 year of historical data)
        print("🚀 Starting data ingestion (1 year of history)...")
        print()

        results = await service.refresh_all_data(days_back=365)

        # Print results
        print()
        print("=" * 70)
        print("📊 INGESTION RESULTS")
        print("=" * 70)
        print()

        # Exchange rates
        if "exchange_rates" in results:
            er = results["exchange_rates"]
            print(f"💱 Exchange Rates:")
            print(f"   Status: {er['status']}")
            print(f"   Records added: {er['records_added']:,}")
            print(f"   Currencies: {', '.join(er['currencies'])}")
            print(f"   Date range: {er['date_range']}")
            print()

        # Central banks
        if "central_banks" in results:
            cb = results["central_banks"]
            print(f"🏦 Central Banks:")
            print(f"   Status: {cb['status']}")
            print(f"   Total records: {cb['records_added']:,}")
            print(f"   Date range: {cb['date_range']}")
            print()
            for bank, count in cb.get("central_banks", {}).items():
                print(f"   {bank}: {count:,} records")
            print()

        # GLI calculation
        if "gli_calculated" in results:
            gli = results["gli_calculated"]
            print(f"🧮 Global Liquidity Index:")
            print(f"   Status: {gli['status']}")
            print(f"   GLI records: {gli['gli_records_added']:,}")
            print()

        # Show latest GLI value
        latest_gli = db.query(GlobalLiquidityIndex).order_by(
            GlobalLiquidityIndex.date.desc()
        ).first()

        if latest_gli:
            print("=" * 70)
            print(f"📈 LATEST GLOBAL LIQUIDITY INDEX")
            print("=" * 70)
            print(f"Date: {latest_gli.date}")
            print(f"Value: ${latest_gli.value:.2f}T USD")
            if latest_gli.change_pct:
                print(f"Change (1-day): {latest_gli.change_pct:+.2f}%")
            if latest_gli.change_1m_pct:
                print(f"Change (1-month): {latest_gli.change_1m_pct:+.2f}%")
            print()

        # Show central bank breakdown for latest date
        if latest_gli:
            print("=" * 70)
            print(f"🌐 CENTRAL BANK BREAKDOWN ({latest_gli.date})")
            print("=" * 70)

            central_banks = ["FED", "ECB", "BOJ", "BOE", "SNB", "BOC", "RBA"]

            for cb in central_banks:
                data = db.query(CentralBankData).filter(
                    CentralBankData.source == cb,
                    CentralBankData.indicator == "balance_sheet",
                    CentralBankData.date == latest_gli.date
                ).first()

                if data:
                    # Get exchange rate if needed
                    value_usd = float(data.value)
                    if data.currency != "USD":
                        exchange_rate = db.query(ExchangeRate).filter(
                            ExchangeRate.from_currency == data.currency,
                            ExchangeRate.date == latest_gli.date
                        ).first()

                        if exchange_rate:
                            value_usd *= float(exchange_rate.rate)
                            print(f"{cb:5} ${value_usd:7.2f}T  ({data.value:.2f}T {data.currency} @ {exchange_rate.rate:.4f})")
                        else:
                            print(f"{cb:5} ${value_usd:7.2f}T  ({data.value:.2f}T {data.currency})")
                    else:
                        print(f"{cb:5} ${value_usd:7.2f}T USD")

            print()

        print("=" * 70)
        print("✅ Data ingestion complete!")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        db.close()

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
