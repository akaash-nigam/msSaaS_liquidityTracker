"""
Ingest private sector liquidity data from FRED

This script fetches priority private sector metrics and calculates:
1. Private Sector Liquidity Index (TPSL)
2. Enhanced Global Liquidity Index (public + private)
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import date, timedelta

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import SessionLocal
from app.services.data_ingestion_service import DataIngestionService


async def main():
    """Main ingestion function"""

    print("=" * 80)
    print("🚀 PRIVATE SECTOR LIQUIDITY DATA INGESTION")
    print("=" * 80)
    print()

    # Create database session
    db = SessionLocal()

    try:
        # Create ingestion service
        service = DataIngestionService(db)

        # Determine date range
        days_back = 365  # 1 year of data
        start_date = date.today() - timedelta(days=days_back)
        end_date = date.today()

        print(f"📅 Date Range: {start_date} to {end_date} ({days_back} days)")
        print()

        # Step 1: Ingest priority private sector data
        print("=" * 80)
        print("STEP 1: Fetching Priority Private Sector Metrics")
        print("=" * 80)
        print()
        print("Fetching 6 priority metrics:")
        print("  1. M2 Money Stock (M2SL)")
        print("  2. Money Market Funds Total (MMMFAQ027S)")
        print("  3. Commercial Paper Total (COMPOUT)")
        print("  4. Primary Dealer Repos (PDREPO)")
        print("  5. Primary Dealer Reverse Repos (PDREVREPO)")
        print("  6. Total Bank Credit (TOTBKCR)")
        print()

        ps_result = await service.ingest_priority_private_sector_data(days_back)

        print()
        print("✅ Private Sector Data Ingestion Complete!")
        print(f"   Status: {ps_result['status']}")
        print(f"   Total Records: {ps_result['records_added']:,}")
        print(f"   Date Range: {ps_result['date_range']}")
        print()
        print("Metrics breakdown:")
        for metric, count in ps_result['metrics'].items():
            print(f"   • {metric}: {count:,} records")
        print()

        # Step 2: Calculate Private Sector Liquidity Index
        print("=" * 80)
        print("STEP 2: Calculating Private Sector Liquidity Index (TPSL)")
        print("=" * 80)
        print()
        print("Formula: TPSL = M2 + MMF + Commercial_Paper + Repos_Net + Bank_Credit")
        print()

        psli_result = await service.calculate_and_store_private_sector_index()

        print()
        print("✅ Private Sector Liquidity Index Calculated!")
        print(f"   Status: {psli_result['status']}")
        print(f"   Index Records: {psli_result['psli_records_added']:,}")
        print()

        # Step 3: Calculate Enhanced Global Liquidity Index
        print("=" * 80)
        print("STEP 3: Calculating Enhanced Global Liquidity Index")
        print("=" * 80)
        print()
        print("Formula: Enhanced_GLI = Central_Bank_Liquidity + Private_Sector_Liquidity")
        print()

        egli_result = await service.calculate_and_store_enhanced_gli()

        print()
        print("✅ Enhanced Global Liquidity Index Calculated!")
        print(f"   Status: {egli_result['status']}")
        print(f"   Index Records: {egli_result['egli_records_added']:,}")
        print()

        # Summary
        print("=" * 80)
        print("📊 INGESTION SUMMARY")
        print("=" * 80)
        print()
        print(f"✅ Private Sector Data: {ps_result['records_added']:,} records")
        print(f"✅ TPSL Index: {psli_result['psli_records_added']:,} records")
        print(f"✅ Enhanced GLI: {egli_result['egli_records_added']:,} records")
        print()

        # Get latest values
        from app.models.private_sector_liquidity import (
            PrivateSectorLiquidityIndex,
            EnhancedGlobalLiquidityIndex
        )

        latest_psli = db.query(PrivateSectorLiquidityIndex).order_by(
            PrivateSectorLiquidityIndex.date.desc()
        ).first()

        latest_egli = db.query(EnhancedGlobalLiquidityIndex).order_by(
            EnhancedGlobalLiquidityIndex.date.desc()
        ).first()

        if latest_psli:
            print("📈 LATEST PRIVATE SECTOR LIQUIDITY INDEX:")
            print(f"   Date: {latest_psli.date}")
            print(f"   Total TPSL: ${float(latest_psli.total_value):.2f} Trillion USD")
            print(f"   Components:")
            if latest_psli.m2_value:
                print(f"     • M2: ${float(latest_psli.m2_value):.2f}T")
            if latest_psli.mmf_value:
                print(f"     • MMF: ${float(latest_psli.mmf_value):.2f}T")
            if latest_psli.commercial_paper_value:
                print(f"     • Commercial Paper: ${float(latest_psli.commercial_paper_value):.2f}T")
            if latest_psli.repos_net_value:
                print(f"     • Repos (Net): ${float(latest_psli.repos_net_value):.2f}T")
            if latest_psli.bank_credit_value:
                print(f"     • Bank Credit: ${float(latest_psli.bank_credit_value):.2f}T")
            print(f"   Data Quality: {latest_psli.data_quality}")
            print()

        if latest_egli:
            print("🌍 LATEST ENHANCED GLOBAL LIQUIDITY INDEX:")
            print(f"   Date: {latest_egli.date}")
            print(f"   Total Enhanced GLI: ${float(latest_egli.total_value):.2f} Trillion USD")
            print(f"   Breakdown:")
            print(f"     • Central Bank Liquidity: ${float(latest_egli.central_bank_liquidity):.2f}T ({float(latest_egli.cb_percentage):.1f}%)")
            print(f"     • Private Sector Liquidity: ${float(latest_egli.private_sector_liquidity):.2f}T ({float(latest_egli.ps_percentage):.1f}%)")
            print()

        print("=" * 80)
        print("✅ ALL DONE!")
        print("=" * 80)
        print()
        print("Next steps:")
        print("  1. Check the /metrics page in your dashboard")
        print("  2. Create API endpoints to serve this data")
        print("  3. Update dashboard to display real metrics")
        print()

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
