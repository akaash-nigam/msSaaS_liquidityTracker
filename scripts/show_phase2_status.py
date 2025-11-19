"""
Show Phase 2 implementation status and what's available
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine, inspect
from app.config import settings


def show_status():
    """Show Phase 2 implementation status"""

    print("=" * 70)
    print("📊 PHASE 2: PRIVATE SECTOR LIQUIDITY - IMPLEMENTATION STATUS")
    print("=" * 70)
    print()

    # Check database connection
    try:
        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print("✅ Database Connection: SUCCESS")
        print(f"   Connected to: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'database'}")
        print()

        # Check for Phase 2 tables
        print("📋 DATABASE TABLES STATUS:")
        print("-" * 70)

        phase2_tables = [
            "private_sector_liquidity",
            "private_sector_liquidity_index",
            "enhanced_global_liquidity_index"
        ]

        for table in phase2_tables:
            if table in tables:
                # Get column count
                columns = inspector.get_columns(table)
                indexes = inspector.get_indexes(table)

                print(f"✅ {table}")
                print(f"   Columns: {len(columns)}")
                print(f"   Indexes: {len(indexes)}")

                # Get row count
                with engine.connect() as conn:
                    result = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    count = result.scalar()
                    print(f"   Records: {count:,}")
            else:
                print(f"❌ {table} - NOT FOUND")
            print()

        # Check existing Phase 1 tables
        print("📋 PHASE 1 TABLES (for reference):")
        print("-" * 70)

        phase1_tables = [
            "central_bank_data",
            "exchange_rates",
            "global_liquidity_index"
        ]

        for table in phase1_tables:
            if table in tables:
                with engine.connect() as conn:
                    result = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    count = result.scalar()
                print(f"✅ {table}: {count:,} records")
            else:
                print(f"❌ {table}: NOT FOUND")

        print()

    except Exception as e:
        print(f"❌ Database Connection: FAILED")
        print(f"   Error: {e}")
        print()

    # Show available metrics
    print()
    print("📊 AVAILABLE PRIVATE SECTOR METRICS:")
    print("-" * 70)

    from app.services.fred_service import FREDService

    fred = FREDService()

    print("\n1. SHADOW BANKING (9 metrics):")
    for key, config in fred.PRIVATE_SECTOR_SERIES["shadow_banking"].items():
        print(f"   • {config['name']}")
        print(f"     Series: {config['series_id']} | Frequency: {config['frequency']}")

    print("\n2. TRADITIONAL BANKING (10 metrics):")
    for key, config in fred.PRIVATE_SECTOR_SERIES["traditional_banking"].items():
        print(f"   • {config['name']}")
        print(f"     Series: {config['series_id']} | Frequency: {config['frequency']}")

    print("\n3. CORPORATE DEBT (3 metrics):")
    for key, config in fred.PRIVATE_SECTOR_SERIES["corporate_debt"].items():
        print(f"   • {config['name']}")
        print(f"     Series: {config['series_id']} | Frequency: {config['frequency']}")

    print()
    print("=" * 70)
    print("📈 PRIORITY METRICS FOR INITIAL IMPLEMENTATION:")
    print("=" * 70)
    print("""
1. M2 Money Stock (M2SL) - Monthly
   → Core broad money supply

2. Money Market Funds Total (MMMFAQ027S) - Quarterly
   → Shadow banking core metric

3. Commercial Paper Total (COMPOUT) - Weekly
   → Short-term corporate funding

4. Primary Dealer Repos (PDREPO) - Weekly
   → Collateral velocity indicator

5. Primary Dealer Reverse Repos (PDREVREPO) - Weekly
   → Collateral velocity (reverse side)

6. Total Bank Credit (TOTBKCR) - Weekly
   → Banking system credit creation
    """)

    print("=" * 70)
    print("🎯 NEXT STEPS:")
    print("=" * 70)
    print("""
1. Run data ingestion script to fetch private sector data
2. Verify data quality and calculations
3. Create API endpoints to serve the data
4. Update frontend dashboard to display metrics

To fetch data, you'll need to:
1. Create an ingestion script (or I can do this for you)
2. Run: python scripts/ingest_private_sector.py
3. Check results in the database
    """)

    print("=" * 70)
    print()


if __name__ == "__main__":
    show_status()
