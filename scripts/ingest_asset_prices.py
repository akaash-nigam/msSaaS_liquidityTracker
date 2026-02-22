"""
Asset Prices & Correlations Data Ingestion Script (Phase 4)
Fetches S&P 500, Gold from FRED; mocks BTC; calculates rolling correlations vs GLI
"""

import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta, datetime
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import SessionLocal
from app.services.fred_service import FREDService
from app.models.asset_prices import AssetPrice, AssetCorrelation
from app.models.base_models import GlobalLiquidityIndex


def calculate_correlation(xs: list, ys: list) -> float:
    """Calculate Pearson correlation between two lists."""
    n = len(xs)
    if n < 5:
        return 0.0
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / n
    std_x = (sum((x - mean_x) ** 2 for x in xs) / n) ** 0.5
    std_y = (sum((y - mean_y) ** 2 for y in ys) / n) ** 0.5
    if std_x == 0 or std_y == 0:
        return 0.0
    return cov / (std_x * std_y)


async def main():
    print("\n" + "=" * 80)
    print("ASSET PRICES & CORRELATIONS DATA INGESTION - PHASE 4")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    db = SessionLocal()
    fred = FREDService()

    end_date = date.today()
    start_date = end_date - timedelta(days=365)

    total_stored = 0

    try:
        # 1. Fetch asset prices
        for key, config in fred.ASSET_PRICE_SERIES.items():
            series_id = config["series_id"]
            print(f"\nFetching {config['name']} ({series_id})...")
            try:
                data = await fred.fetch_series(series_id, start_date, end_date)
                observations = data.get("observations", [])
                print(f"  Retrieved {len(observations)} data points")

                count = 0
                for obs in observations:
                    existing = db.query(AssetPrice).filter(
                        AssetPrice.asset_name == config["name"],
                        AssetPrice.date == obs["date"],
                    ).first()
                    if not existing:
                        db.add(AssetPrice(
                            date=obs["date"],
                            asset_name=config["name"],
                            ticker=config["ticker"],
                            price=Decimal(str(obs["value"])),
                            asset_class=config["asset_class"],
                            data_source="FRED",
                        ))
                        count += 1

                db.commit()
                print(f"  Stored {count} new records")
                total_stored += count

            except Exception as e:
                print(f"  Error: {e}")
                db.rollback()

        # 2. Calculate correlations vs GLI
        print("\nCalculating correlations vs GLI...")

        # Get GLI time series
        gli_rows = (
            db.query(GlobalLiquidityIndex)
            .filter(GlobalLiquidityIndex.date >= start_date)
            .order_by(GlobalLiquidityIndex.date)
            .all()
        )
        gli_by_date = {r.date: float(r.value) for r in gli_rows}

        for key, config in fred.ASSET_PRICE_SERIES.items():
            print(f"  Correlations for {config['name']}...")

            asset_rows = (
                db.query(AssetPrice)
                .filter(
                    AssetPrice.asset_name == config["name"],
                    AssetPrice.date >= start_date,
                )
                .order_by(AssetPrice.date)
                .all()
            )

            if not asset_rows:
                print("    No price data, skipping")
                continue

            asset_by_date = {r.date: float(r.price) for r in asset_rows}

            # Find common dates
            common_dates = sorted(set(gli_by_date.keys()) & set(asset_by_date.keys()))

            if len(common_dates) < 10:
                print(f"    Only {len(common_dates)} common dates, skipping")
                continue

            # Calculate rolling correlations
            latest_date = common_dates[-1]

            def get_corr(window_days: int) -> float:
                cutoff = latest_date - timedelta(days=window_days)
                window_dates = [d for d in common_dates if d >= cutoff]
                if len(window_dates) < 5:
                    return 0.0
                xs = [gli_by_date[d] for d in window_dates]
                ys = [asset_by_date[d] for d in window_dates]
                return round(calculate_correlation(xs, ys), 6)

            corr_30 = get_corr(30)
            corr_90 = get_corr(90)
            corr_365 = get_corr(365)

            # Beta = correlation * (std_asset / std_gli)
            window_dates = [d for d in common_dates if d >= latest_date - timedelta(days=90)]
            if len(window_dates) >= 5:
                xs = [gli_by_date[d] for d in window_dates]
                ys = [asset_by_date[d] for d in window_dates]
                mean_x = sum(xs) / len(xs)
                mean_y = sum(ys) / len(ys)
                std_x = (sum((x - mean_x) ** 2 for x in xs) / len(xs)) ** 0.5
                std_y = (sum((y - mean_y) ** 2 for y in ys) / len(ys)) ** 0.5
                beta = round(corr_90 * (std_y / std_x), 6) if std_x > 0 else 0.0
            else:
                beta = 0.0

            # Store correlation
            existing = db.query(AssetCorrelation).filter(
                AssetCorrelation.asset_name == config["name"],
                AssetCorrelation.date == latest_date,
            ).first()

            if not existing:
                db.add(AssetCorrelation(
                    date=latest_date,
                    asset_name=config["name"],
                    correlation_30d=Decimal(str(corr_30)),
                    correlation_90d=Decimal(str(corr_90)),
                    correlation_365d=Decimal(str(corr_365)),
                    beta_to_gli=Decimal(str(beta)),
                    gli_value=Decimal(str(gli_by_date.get(latest_date, 0))),
                ))
                db.commit()
                print(f"    30d={corr_30:.3f}  90d={corr_90:.3f}  365d={corr_365:.3f}  beta={beta:.3f}")
            else:
                print("    Correlation already exists for latest date")

        print("\n" + "=" * 80)
        print("ASSET PRICES & CORRELATIONS INGESTION COMPLETE")
        print("=" * 80)
        print(f"Total Price Records Stored: {total_stored}")
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
