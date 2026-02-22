"""GLI (Global Liquidity Index) endpoints."""

from datetime import date, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.base_models import CentralBankData, GlobalLiquidityIndex, ExchangeRate
from app.models.private_sector_liquidity import EnhancedGlobalLiquidityIndex

from .helpers import TIMEFRAME_DAYS, _cycle_position

router = APIRouter()


# ---------------------------------------------------------------------------
# Mock data helpers
# ---------------------------------------------------------------------------

def _mock_gli_current() -> dict:
    return {
        "date": date.today().isoformat(),
        "value": 85.2,
        "change_pct": 0.12,
        "change_1m_pct": 1.34,
        "cycle_position": "expansion",
        "num_sources": 8,
        "cb_value": 32.7,
        "ps_value": 52.5,
    }


def _mock_gli_historical(days: int) -> list:
    import random
    random.seed(42)
    points, value, current = [], 74.0, date.today() - timedelta(days=days)
    while current <= date.today():
        if current.weekday() < 5:
            value += random.uniform(-0.3, 0.35)
            points.append({"date": current.isoformat(), "value": round(value, 2)})
        current += timedelta(days=1)
    return points


def _mock_gli_components() -> list:
    return [
        {"source": "FED", "value": 7.5, "currency": "USD", "value_usd": 7.5, "pct_of_total": 22.9},
        {"source": "ECB", "value": 6.8, "currency": "EUR", "value_usd": 7.34, "pct_of_total": 22.4},
        {"source": "PBOC", "value": 49.3, "currency": "CNY", "value_usd": 6.80, "pct_of_total": 20.8},
        {"source": "BOJ", "value": 750, "currency": "JPY", "value_usd": 5.0, "pct_of_total": 15.3},
        {"source": "BOE", "value": 0.85, "currency": "GBP", "value_usd": 1.08, "pct_of_total": 3.3},
        {"source": "SNB", "value": 0.8, "currency": "CHF", "value_usd": 0.90, "pct_of_total": 2.8},
        {"source": "RBA", "value": 0.55, "currency": "AUD", "value_usd": 0.36, "pct_of_total": 1.1},
        {"source": "BOC", "value": 0.4, "currency": "CAD", "value_usd": 0.29, "pct_of_total": 0.9},
    ]


def _mock_cycle_data() -> dict:
    return {
        "current_position": "expansion",
        "momentum": 1.34,
        "cycle_day": 820,
        "total_cycle_days": 1975,
        "phase_pct": 41.5,
    }


def _mock_gli_historical_stacked(days: int) -> list:
    import random
    random.seed(77)
    points, cb, ps = [], 24.0, 50.0
    current = date.today() - timedelta(days=days)
    while current <= date.today():
        if current.weekday() < 5:
            cb += random.uniform(-0.1, 0.12)
            ps += random.uniform(-0.15, 0.2)
            points.append({
                "date": current.isoformat(),
                "cb_value": round(cb, 2),
                "ps_value": round(ps, 2),
            })
        current += timedelta(days=1)
    return points


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/gli/current")
def get_gli_current(db: Session = Depends(get_db)):
    """Current Global Liquidity Index (Enhanced when available)."""
    try:
        enhanced = (
            db.query(EnhancedGlobalLiquidityIndex)
            .order_by(EnhancedGlobalLiquidityIndex.date.desc())
            .first()
        )
        if enhanced:
            value = float(enhanced.total_value)
            change_pct = float(enhanced.change_pct) if enhanced.change_pct else 0
            change_1m = float(enhanced.change_1m_pct) if enhanced.change_1m_pct else 0
            return {
                "date": enhanced.date.isoformat(),
                "value": round(value, 2),
                "change_pct": round(change_pct, 2),
                "change_1m_pct": round(change_1m, 2),
                "cycle_position": _cycle_position(change_1m),
                "num_sources": 8,
                "cb_value": round(float(enhanced.central_bank_liquidity), 2),
                "ps_value": round(float(enhanced.private_sector_liquidity), 2),
            }

        latest = (
            db.query(GlobalLiquidityIndex)
            .order_by(GlobalLiquidityIndex.date.desc())
            .first()
        )
    except Exception:
        return _mock_gli_current()

    if not latest:
        return _mock_gli_current()

    value = float(latest.value)
    change_1m = float(latest.change_1m_pct) if latest.change_1m_pct else 0
    return {
        "date": latest.date.isoformat(),
        "value": round(value, 2),
        "change_pct": round(float(latest.change_pct), 2) if latest.change_pct else 0,
        "change_1m_pct": round(change_1m, 2),
        "cycle_position": _cycle_position(change_1m),
        "num_sources": latest.num_sources or 7,
    }


@router.get("/gli/historical")
def get_gli_historical(
    timeframe: str = Query("1Y", regex="^(1M|3M|6M|1Y|2Y|5Y|ALL)$"),
    db: Session = Depends(get_db),
):
    """Historical GLI time series."""
    days = TIMEFRAME_DAYS.get(timeframe, 365)
    cutoff = date.today() - timedelta(days=days)
    try:
        rows = (
            db.query(EnhancedGlobalLiquidityIndex)
            .filter(EnhancedGlobalLiquidityIndex.date >= cutoff)
            .order_by(EnhancedGlobalLiquidityIndex.date)
            .all()
        )
        if rows:
            return [{"date": r.date.isoformat(), "value": round(float(r.total_value), 2)} for r in rows]

        rows = (
            db.query(GlobalLiquidityIndex)
            .filter(GlobalLiquidityIndex.date >= cutoff)
            .order_by(GlobalLiquidityIndex.date)
            .all()
        )
    except Exception:
        return _mock_gli_historical(days)

    if not rows:
        return _mock_gli_historical(days)
    return [{"date": r.date.isoformat(), "value": round(float(r.value), 2)} for r in rows]


@router.get("/gli/components")
def get_gli_components(db: Session = Depends(get_db)):
    """Central bank component breakdown."""
    try:
        latest_gli = db.query(GlobalLiquidityIndex).order_by(GlobalLiquidityIndex.date.desc()).first()
    except Exception:
        return _mock_gli_components()
    if not latest_gli:
        return _mock_gli_components()

    d = latest_gli.date
    banks = db.query(CentralBankData).filter(CentralBankData.date == d, CentralBankData.indicator == "balance_sheet").all()
    total_usd = Decimal("0")
    components = []
    for b in banks:
        val_usd = b.value
        if b.currency != "USD":
            fx = db.query(ExchangeRate).filter(ExchangeRate.from_currency == b.currency, ExchangeRate.date == d).first()
            if fx:
                val_usd = b.value * fx.rate
        total_usd += val_usd
        components.append({"source": b.source, "value": round(float(b.value), 2), "currency": b.currency, "value_usd": round(float(val_usd), 2)})

    for c in components:
        c["pct_of_total"] = round(c["value_usd"] / float(total_usd) * 100, 1) if total_usd else 0
    components.sort(key=lambda x: x["value_usd"], reverse=True)
    return components


@router.get("/gli/cycle")
def get_gli_cycle(db: Session = Depends(get_db)):
    """Current cycle position and momentum."""
    try:
        latest = db.query(EnhancedGlobalLiquidityIndex).order_by(EnhancedGlobalLiquidityIndex.date.desc()).first()
        if not latest:
            latest = db.query(GlobalLiquidityIndex).order_by(GlobalLiquidityIndex.date.desc()).first()
        if not latest:
            return _mock_cycle_data()

        change_1m = float(latest.change_1m_pct) if latest.change_1m_pct else 0

        earliest = db.query(GlobalLiquidityIndex).order_by(GlobalLiquidityIndex.date).first()
        if earliest:
            cycle_day = (latest.date - earliest.date).days
        else:
            cycle_day = 0
        total_cycle_days = 1975
        phase_pct = round((cycle_day % total_cycle_days) / total_cycle_days * 100, 1)

        return {
            "current_position": _cycle_position(change_1m),
            "momentum": round(change_1m, 2),
            "cycle_day": cycle_day % total_cycle_days,
            "total_cycle_days": total_cycle_days,
            "phase_pct": phase_pct,
        }
    except Exception:
        return _mock_cycle_data()


@router.get("/gli/historical-stacked")
def get_gli_historical_stacked(
    timeframe: str = Query("1Y", regex="^(1M|3M|6M|1Y|2Y|5Y|ALL)$"),
    db: Session = Depends(get_db),
):
    """Historical CB vs Private Sector liquidity breakdown."""
    days = TIMEFRAME_DAYS.get(timeframe, 365)
    cutoff = date.today() - timedelta(days=days)
    try:
        rows = (
            db.query(EnhancedGlobalLiquidityIndex)
            .filter(EnhancedGlobalLiquidityIndex.date >= cutoff)
            .order_by(EnhancedGlobalLiquidityIndex.date)
            .all()
        )
        if rows:
            return [
                {
                    "date": r.date.isoformat(),
                    "cb_value": round(float(r.central_bank_liquidity), 2),
                    "ps_value": round(float(r.private_sector_liquidity), 2),
                }
                for r in rows
            ]
    except Exception:
        pass
    return _mock_gli_historical_stacked(days)
