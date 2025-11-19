"""
Show real data we've ingested
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine, func
from app.config import settings
from app.models.private_sector_liquidity import (
    PrivateSectorLiquidity,
    PrivateSectorLiquidityIndex,
    EnhancedGlobalLiquidityIndex
)
from sqlalchemy.orm import sessionmaker

# Create session
engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

print("=" * 80)
print("📊 REAL DATA IN DATABASE")
print("=" * 80)
print()

# Count records by series
print("📈 RAW METRICS DATA:")
print("-" * 80)

metrics_count = db.query(
    PrivateSectorLiquidity.series_id,
    PrivateSectorLiquidity.metric_name,
    func.count(PrivateSectorLiquidity.id).label('count'),
    func.min(PrivateSectorLiquidity.date).label('min_date'),
    func.max(PrivateSectorLiquidity.date).label('max_date')
).group_by(
    PrivateSectorLiquidity.series_id,
    PrivateSectorLiquidity.metric_name
).all()

total_records = 0
for series_id, name, count, min_date, max_date in metrics_count:
    print(f"✅ {name}")
    print(f"   Series: {series_id} | Records: {count} | From {min_date} to {max_date}")
    total_records += count

print()
print(f"📊 Total Raw Metric Records: {total_records:,}")
print()

# Show latest values
print("=" * 80)
print("💰 LATEST METRIC VALUES (Real Data from FRED)")
print("=" * 80)
print()

latest_metrics = db.query(PrivateSectorLiquidity).order_by(
    PrivateSectorLiquidity.series_id,
    PrivateSectorLiquidity.date.desc()
).distinct(PrivateSectorLiquidity.series_id).all()

for metric in latest_metrics:
    value_trillions = float(metric.value) / 1000  # Convert billions to trillions
    print(f"📊 {metric.metric_name}")
    print(f"   Date: {metric.date}")
    print(f"   Value: ${float(metric.value):,.2f} Billion USD (${value_trillions:.3f} Trillion)")
    print(f"   Frequency: {metric.frequency}")
    print()

# Check calculated indices
psli_count = db.query(func.count(PrivateSectorLiquidityIndex.id)).scalar()
egli_count = db.query(func.count(EnhancedGlobalLiquidityIndex.id)).scalar()

print("=" * 80)
print("🧮 CALCULATED INDICES")
print("=" * 80)
print()
print(f"Private Sector Liquidity Index (TPSL): {psli_count:,} records")
print(f"Enhanced Global Liquidity Index: {egli_count:,} records")
print()

# Show latest TPSL if exists
if psli_count > 0:
    latest_psli = db.query(PrivateSectorLiquidityIndex).order_by(
        PrivateSectorLiquidityIndex.date.desc()
    ).first()

    print("📈 LATEST PRIVATE SECTOR LIQUIDITY INDEX (TPSL):")
    print(f"   Date: {latest_psli.date}")
    print(f"   Total: ${float(latest_psli.total_value):.3f} Trillion USD")
    print()
    print("   Components:")
    if latest_psli.m2_value:
        print(f"     • M2: ${float(latest_psli.m2_value):.3f}T")
    if latest_psli.mmf_value:
        print(f"     • MMF: ${float(latest_psli.mmf_value):.3f}T")
    if latest_psli.commercial_paper_value:
        print(f"     • Commercial Paper: ${float(latest_psli.commercial_paper_value):.3f}T")
    if latest_psli.repos_net_value:
        print(f"     • Repos (Net): ${float(latest_psli.repos_net_value):.3f}T")
    if latest_psli.bank_credit_value:
        print(f"     • Bank Credit: ${float(latest_psli.bank_credit_value):.3f}T")
    print()

# Show latest Enhanced GLI if exists
if egli_count > 0:
    latest_egli = db.query(EnhancedGlobalLiquidityIndex).order_by(
        EnhancedGlobalLiquidityIndex.date.desc()
    ).first()

    print("🌍 LATEST ENHANCED GLOBAL LIQUIDITY INDEX:")
    print(f"   Date: {latest_egli.date}")
    print(f"   Total: ${float(latest_egli.total_value):.2f} Trillion USD")
    print()
    print("   Breakdown:")
    print(f"     • Central Bank: ${float(latest_egli.central_bank_liquidity):.2f}T ({float(latest_egli.cb_percentage):.1f}%)")
    print(f"     • Private Sector: ${float(latest_egli.private_sector_liquidity):.2f}T ({float(latest_egli.ps_percentage):.1f}%)")
    print()

print("=" * 80)

db.close()
