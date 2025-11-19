"""
Initialize asset prices and correlation tables

This script creates the new tables needed for Phase 7:
- asset_prices: Historical prices for tracked assets
- asset_correlations: Rolling correlations with GLI
"""

from app.database import engine, Base
from app.models.asset_prices import AssetPrice, AssetCorrelation

def init_asset_tables():
    """Create asset-related tables"""
    print("=" * 80)
    print("🎯 PHASE 7: INITIALIZING ASSET CORRELATION TABLES")
    print("=" * 80)
    print()

    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        print("✅ Successfully created tables:")
        print("   - asset_prices")
        print("   - asset_correlations")
        print()
        print("📊 Ready to track asset correlations with GLI!")
        print()

    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_asset_tables()
