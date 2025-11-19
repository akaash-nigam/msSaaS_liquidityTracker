"""
Capital Flows Data Ingestion Script (Phase 3A)
Fetches US TIC and Balance of Payments data from FRED
"""

import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta, datetime
from decimal import Decimal

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import SessionLocal
from app.services.fred_service import FREDService
from app.models.capital_flows import CapitalFlow, USTreasuryTIC, BalanceOfPayments


async def ingest_us_treasury_tic_data(db, fred_service):
    """
    Ingest US Treasury TIC (Treasury International Capital) data
    Foreign holdings of US assets
    """
    print("\n" + "="*80)
    print("📊 INGESTING US TREASURY TIC DATA")
    print("="*80)

    # Fetch last 10 years of data
    end_date = date.today()
    start_date = end_date - timedelta(days=3650)  # 10 years

    # Priority TIC series
    tic_series = {
        "total_assets": ("rest_of_world", "total_financial_assets"),
        "treasuries": ("rest_of_world", "treasury_securities"),
        "equities": ("rest_of_world", "corporate_equities"),
        "corporate_bonds": ("rest_of_world", "corporate_bonds"),
        "agency_securities": ("rest_of_world", "agency_securities")
    }

    all_tic_data = {}

    # Fetch all series
    for series_name, (category, subcategory) in tic_series.items():
        print(f"\n🔍 Fetching {series_name}...")
        try:
            data = await fred_service.fetch_capital_flows_metric(
                category, subcategory, start_date, end_date
            )
            all_tic_data[series_name] = data
            print(f"✅ Retrieved {len(data['observations'])} data points")
        except Exception as e:
            print(f"❌ Error: {e}")
            all_tic_data[series_name] = {"observations": []}

    # Store in database - aggregate by date
    print("\n💾 Storing TIC data in database...")

    # Get all unique dates
    all_dates = set()
    for series_data in all_tic_data.values():
        for obs in series_data.get("observations", []):
            all_dates.add(obs["date"])

    stored_count = 0
    updated_count = 0

    for report_date in sorted(all_dates):
        # Aggregate data for this date
        treasuries_total = None
        equities = None
        corporate_bonds = None
        agency = None
        total_holdings = None

        # Get values for this date from each series
        for series_name, series_data in all_tic_data.items():
            matching_obs = [o for o in series_data.get("observations", []) if o["date"] == report_date]
            if matching_obs:
                value = Decimal(str(matching_obs[0]["value"]))

                if series_name == "total_assets":
                    total_holdings = value
                elif series_name == "treasuries":
                    treasuries_total = value
                elif series_name == "equities":
                    equities = value
                elif series_name == "corporate_bonds":
                    corporate_bonds = value
                elif series_name == "agency_securities":
                    agency = value

        # Only store if we have the total holdings value
        if total_holdings is None:
            continue

        # Check if record exists
        existing = db.query(USTreasuryTIC).filter(
            USTreasuryTIC.country_code == "ROW",  # Rest of World
            USTreasuryTIC.report_date == report_date
        ).first()

        if existing:
            # Update existing record
            existing.total_treasuries = treasuries_total
            existing.equities = equities
            existing.corporate_bonds = corporate_bonds
            existing.agency_bonds = agency
            existing.total_holdings = total_holdings
            existing.series_id = all_tic_data["total_assets"].get("series_id")
            updated_count += 1
        else:
            # Create new record
            tic_record = USTreasuryTIC(
                report_date=report_date,
                country_code="ROW",  # Rest of World aggregate
                country_name="Rest of World",
                treasury_bonds=None,  # We don't separate bonds vs bills in this data
                treasury_bills=None,
                total_treasuries=treasuries_total,
                agency_bonds=agency,
                corporate_bonds=corporate_bonds,
                equities=equities,
                total_holdings=total_holdings,
                series_id=all_tic_data["total_assets"].get("series_id"),
                data_source="US_TREASURY_TIC"
            )
            db.add(tic_record)
            stored_count += 1

    db.commit()
    print(f"✅ Stored {stored_count} new TIC records, updated {updated_count} existing records")

    return stored_count + updated_count


async def ingest_balance_of_payments_data(db, fred_service):
    """
    Ingest US Balance of Payments data
    """
    print("\n" + "="*80)
    print("📊 INGESTING US BALANCE OF PAYMENTS DATA")
    print("="*80)

    end_date = date.today()
    start_date = end_date - timedelta(days=3650)  # 10 years

    # BOP series
    bop_series = {
        "trade_balance": ("balance_of_payments", "trade_balance"),
        "current_account": ("balance_of_payments", "current_account"),
        "financial_account": ("balance_of_payments", "financial_account"),
        "net_financial_inflows": ("balance_of_payments", "net_financial_inflows"),
        "fdi_net": ("balance_of_payments", "fdi_net"),
        "portfolio_investment_net": ("balance_of_payments", "portfolio_investment_net")
    }

    all_bop_data = {}

    # Fetch all series
    for series_name, (category, subcategory) in bop_series.items():
        print(f"\n🔍 Fetching {series_name}...")
        try:
            data = await fred_service.fetch_capital_flows_metric(
                category, subcategory, start_date, end_date
            )
            all_bop_data[series_name] = data
            print(f"✅ Retrieved {len(data['observations'])} data points")
        except Exception as e:
            print(f"❌ Error: {e}")
            all_bop_data[series_name] = {"observations": []}

    # Store in database
    print("\n💾 Storing BOP data in database...")

    # Get all unique dates
    all_dates = set()
    for series_data in all_bop_data.values():
        for obs in series_data.get("observations", []):
            all_dates.add(obs["date"])

    stored_count = 0
    updated_count = 0

    for report_date in sorted(all_dates):
        # Aggregate data for this date
        trade_bal = None
        current_acct = None
        financial_acct = None
        net_fin_inflows = None
        fdi = None
        portfolio = None

        # Get values for this date from each series
        for series_name, series_data in all_bop_data.items():
            matching_obs = [o for o in series_data.get("observations", []) if o["date"] == report_date]
            if matching_obs:
                # BOP data is in millions USD, convert to billions
                value = Decimal(str(matching_obs[0]["value"])) / 1000

                if series_name == "trade_balance":
                    trade_bal = value
                elif series_name == "current_account":
                    current_acct = value
                elif series_name == "financial_account":
                    financial_acct = value
                elif series_name == "net_financial_inflows":
                    net_fin_inflows = value
                elif series_name == "fdi_net":
                    fdi = value
                elif series_name == "portfolio_investment_net":
                    portfolio = value

        # Check if record exists
        existing = db.query(BalanceOfPayments).filter(
            BalanceOfPayments.country_code == "USA",
            BalanceOfPayments.report_date == report_date
        ).first()

        if existing:
            # Update existing record
            existing.trade_balance = trade_bal
            existing.current_account_balance = current_acct
            existing.financial_account_balance = financial_acct
            existing.net_direct_investment = fdi
            existing.net_portfolio_investment = portfolio
            updated_count += 1
        else:
            # Create new record
            bop_record = BalanceOfPayments(
                report_date=report_date,
                country_code="USA",
                country_name="United States",
                current_account_balance=current_acct,
                trade_balance=trade_bal,
                goods_exports=None,  # Could add these series later
                goods_imports=None,
                services_balance=None,
                primary_income=None,
                secondary_income=None,
                capital_account_balance=None,
                financial_account_balance=financial_acct,
                direct_investment_abroad=None,  # We have net FDI only
                direct_investment_inward=None,
                net_direct_investment=fdi,
                portfolio_investment_assets=None,  # We have net portfolio only
                portfolio_investment_liabilities=None,
                net_portfolio_investment=portfolio,
                other_investment_assets=None,
                other_investment_liabilities=None,
                net_other_investment=None,
                reserve_assets=None,
                net_errors_omissions=None,
                series_id=all_bop_data["current_account"].get("series_id") if "current_account" in all_bop_data else None,
                data_source="IMF_BOP",
                frequency="quarterly"
            )
            db.add(bop_record)
            stored_count += 1

    db.commit()
    print(f"✅ Stored {stored_count} new BOP records, updated {updated_count} existing records")

    return stored_count + updated_count


async def ingest_capital_flow_metrics(db, fred_service):
    """
    Ingest capital flow metrics into CapitalFlow table
    (More granular storage of individual series)
    """
    print("\n" + "="*80)
    print("📊 INGESTING CAPITAL FLOW METRICS")
    print("="*80)

    end_date = date.today()
    start_date = end_date - timedelta(days=3650)  # 10 years

    # Fetch priority capital flows data
    priority_data = await fred_service.fetch_priority_capital_flows_data(start_date, end_date)

    stored_count = 0

    for metric_key, metric_data in priority_data.items():
        if "error" in metric_data:
            print(f"⚠️  Skipping {metric_key} due to error")
            continue

        observations = metric_data.get("observations", [])
        print(f"\n📈 Processing {metric_key}: {len(observations)} observations")

        for obs in observations:
            flow_date = obs["date"]
            value_billions = Decimal(str(obs["value"]))

            # Convert millions to billions if needed
            if metric_data.get("unit") == "millions_usd":
                value_billions = value_billions / 1000

            # Determine flow type and direction
            flow_type = "portfolio_equity" if "equity" in metric_key else "portfolio_debt" if "treasury" in metric_key else "other"
            direction = "net"

            # Adjust for BOP series
            if "balance" in metric_key or "account" in metric_key:
                flow_type = "official"
                direction = "net"

            # Check if record exists
            existing = db.query(CapitalFlow).filter(
                CapitalFlow.series_id == metric_data.get("series_id"),
                CapitalFlow.flow_date == flow_date
            ).first()

            if not existing:
                flow_record = CapitalFlow(
                    flow_date=flow_date,
                    source_country=None,  # Aggregate data, not country-specific
                    destination_country="USA",
                    region_from=None,
                    region_to="north_america",
                    flow_type=flow_type,
                    asset_class="equity" if "equity" in metric_key else "debt",
                    sector="government" if "official" in metric_key else "non_bank_financial",
                    direction=direction,
                    amount_usd=value_billions,
                    amount_local=None,
                    currency="USD",
                    data_source=metric_data.get("data_category", "FRED_TIC"),
                    series_id=metric_data.get("series_id"),
                    frequency=metric_data.get("frequency", "quarterly")
                )
                db.add(flow_record)
                stored_count += 1

    db.commit()
    print(f"\n✅ Stored {stored_count} capital flow records")

    return stored_count


async def main():
    """Main ingestion workflow"""
    print("\n" + "="*80)
    print("🌍 CAPITAL FLOWS DATA INGESTION - PHASE 3A")
    print("="*80)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    db = SessionLocal()
    fred_service = FREDService()

    try:
        # 1. Ingest US Treasury TIC Data
        tic_count = await ingest_us_treasury_tic_data(db, fred_service)

        # 2. Ingest Balance of Payments Data
        bop_count = await ingest_balance_of_payments_data(db, fred_service)

        # 3. Ingest Capital Flow Metrics
        flow_count = await ingest_capital_flow_metrics(db, fred_service)

        # Summary
        print("\n" + "="*80)
        print("✅ CAPITAL FLOWS INGESTION COMPLETE")
        print("="*80)
        print(f"📊 US Treasury TIC Records: {tic_count}")
        print(f"📊 Balance of Payments Records: {bop_count}")
        print(f"📊 Capital Flow Metrics: {flow_count}")
        print(f"📊 Total Records: {tic_count + bop_count + flow_count}")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
