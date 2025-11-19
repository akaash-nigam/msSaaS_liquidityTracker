"""
Create Capital Flows Database Tables (Phase 3A)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import engine, Base
from app.models.capital_flows import (
    CapitalFlow,
    CapitalFlowIndex,
    USTreasuryTIC,
    BISBankingFlows,
    BalanceOfPayments
)


def create_tables():
    """Create all capital flows related tables"""
    print("="*80)
    print("🗄️  CREATING CAPITAL FLOWS TABLES")
    print("="*80)

    try:
        print("\n📋 Tables to be created:")
        print("  1. capital_flows - Raw capital flow transactions")
        print("  2. capital_flow_index - Aggregated daily/monthly indices")
        print("  3. us_treasury_tic - US Treasury International Capital data")
        print("  4. bis_banking_flows - BIS cross-border banking statistics")
        print("  5. balance_of_payments - IMF Balance of Payments data")

        print("\n🔨 Creating tables...")
        Base.metadata.create_all(bind=engine)

        print("\n✅ All capital flows tables created successfully!")
        print("="*80)

        print("\n📊 Table Schemas:")
        print("\n1. capital_flows:")
        print("   - id, flow_date, source_country, destination_country")
        print("   - flow_type, asset_class, sector, direction")
        print("   - amount_usd, currency, data_source, series_id")

        print("\n2. capital_flow_index:")
        print("   - id, index_date, total_global_flows")
        print("   - dm_to_em_flows, em_to_dm_flows")
        print("   - us_net_flows, risk_appetite_score")
        print("   - dollar_strength_index, capital_flight_index")

        print("\n3. us_treasury_tic:")
        print("   - id, report_date, country_code, country_name")
        print("   - total_treasuries, equities, corporate_bonds")
        print("   - total_holdings, mom_change, yoy_change")

        print("\n4. bis_banking_flows:")
        print("   - id, report_date, reporting_country")
        print("   - counterparty_country, currency")
        print("   - cross_border_claims, cross_border_liabilities")

        print("\n5. balance_of_payments:")
        print("   - id, report_date, country_code")
        print("   - current_account_balance, trade_balance")
        print("   - financial_account_balance, net_direct_investment")
        print("   - net_portfolio_investment, reserve_assets")

        print("\n🎯 Next Steps:")
        print("   1. Run: python scripts/ingest_capital_flows.py")
        print("   2. Verify data: Check database tables for records")
        print("   3. Create API endpoints to expose the data")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    create_tables()
