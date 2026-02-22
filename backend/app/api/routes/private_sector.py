"""Private Sector Liquidity endpoints."""

from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.private_sector_liquidity import PrivateSectorLiquidityIndex

from .helpers import TIMEFRAME_DAYS

router = APIRouter()


# ---------------------------------------------------------------------------
# Mock data helpers
# ---------------------------------------------------------------------------

def _mock_private_sector_current() -> dict:
    return {
        "date": date.today().isoformat(),
        "total_value": 52.5,
        "change_pct": 0.08,
        "change_1m_pct": 0.95,
        "data_quality": "full",
        "num_components": 5,
        "components": {"m2": 23.9, "mmf": 6.9, "commercial_paper": 1.4, "repos_net": 0.8, "bank_credit": 19.1},
    }


def _mock_private_sector_historical(days: int) -> list:
    import random
    random.seed(99)
    points, value, current = [], 50.0, date.today() - timedelta(days=days)
    while current <= date.today():
        if current.weekday() < 5:
            value += random.uniform(-0.1, 0.15)
            points.append({"date": current.isoformat(), "value": round(value, 2)})
        current += timedelta(days=1)
    return points


def _mock_private_sector_components() -> list:
    return [
        {"name": "M2 Money Stock", "key": "m2", "value": 23.9, "pct_of_total": 45.5},
        {"name": "Total Bank Credit", "key": "bank_credit", "value": 19.1, "pct_of_total": 36.4},
        {"name": "Money Market Funds", "key": "mmf", "value": 6.9, "pct_of_total": 13.1},
        {"name": "Commercial Paper", "key": "commercial_paper", "value": 1.4, "pct_of_total": 2.7},
        {"name": "Net Repos", "key": "repos_net", "value": 0.8, "pct_of_total": 1.5},
    ]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/private-sector/current")
def get_private_sector_current(db: Session = Depends(get_db)):
    """Latest TPSL value with component breakdown."""
    try:
        latest = db.query(PrivateSectorLiquidityIndex).order_by(PrivateSectorLiquidityIndex.date.desc()).first()
    except Exception:
        return _mock_private_sector_current()
    if not latest:
        return _mock_private_sector_current()

    return {
        "date": latest.date.isoformat(),
        "total_value": round(float(latest.total_value), 2),
        "change_pct": round(float(latest.change_pct), 2) if latest.change_pct else 0,
        "change_1m_pct": round(float(latest.change_1m_pct), 2) if latest.change_1m_pct else 0,
        "data_quality": latest.data_quality or "partial",
        "num_components": latest.num_components or 0,
        "components": {
            "m2": round(float(latest.m2_value), 2) if latest.m2_value else 0,
            "mmf": round(float(latest.mmf_value), 2) if latest.mmf_value else 0,
            "commercial_paper": round(float(latest.commercial_paper_value), 2) if latest.commercial_paper_value else 0,
            "repos_net": round(float(latest.repos_net_value), 2) if latest.repos_net_value else 0,
            "bank_credit": round(float(latest.bank_credit_value), 2) if latest.bank_credit_value else 0,
        },
    }


@router.get("/private-sector/historical")
def get_private_sector_historical(
    timeframe: str = Query("1Y", regex="^(1M|3M|6M|1Y|2Y|5Y|ALL)$"),
    db: Session = Depends(get_db),
):
    """TPSL historical time series."""
    days = TIMEFRAME_DAYS.get(timeframe, 365)
    cutoff = date.today() - timedelta(days=days)
    try:
        rows = (
            db.query(PrivateSectorLiquidityIndex)
            .filter(PrivateSectorLiquidityIndex.date >= cutoff)
            .order_by(PrivateSectorLiquidityIndex.date)
            .all()
        )
    except Exception:
        return _mock_private_sector_historical(days)
    if not rows:
        return _mock_private_sector_historical(days)
    return [{"date": r.date.isoformat(), "value": round(float(r.total_value), 2)} for r in rows]


@router.get("/private-sector/components")
def get_private_sector_components(db: Session = Depends(get_db)):
    """TPSL component breakdown."""
    try:
        latest = db.query(PrivateSectorLiquidityIndex).order_by(PrivateSectorLiquidityIndex.date.desc()).first()
    except Exception:
        return _mock_private_sector_components()
    if not latest:
        return _mock_private_sector_components()

    total = float(latest.total_value)
    items = [
        ("M2 Money Stock", "m2", latest.m2_value),
        ("Total Bank Credit", "bank_credit", latest.bank_credit_value),
        ("Money Market Funds", "mmf", latest.mmf_value),
        ("Commercial Paper", "commercial_paper", latest.commercial_paper_value),
        ("Net Repos", "repos_net", latest.repos_net_value),
    ]
    result = []
    for name, key, val in items:
        v = round(float(val), 2) if val else 0
        result.append({"name": name, "key": key, "value": v, "pct_of_total": round(v / total * 100, 1) if total else 0})
    return result
