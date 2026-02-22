"""Fed RRP and Balance Sheet endpoints."""

from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.base_models import CentralBankData

from .helpers import TIMEFRAME_DAYS

router = APIRouter()


# ---------------------------------------------------------------------------
# Mock data helpers
# ---------------------------------------------------------------------------

def _mock_fed_rrp() -> dict:
    import random
    random.seed(55)
    history = []
    val = 500.0
    current = date.today() - timedelta(days=90)
    while current <= date.today():
        if current.weekday() < 5:
            val = max(50, val + random.uniform(-20, 10))
            history.append({"date": current.isoformat(), "value": round(val, 1)})
        current += timedelta(days=1)
    return {
        "date": date.today().isoformat(),
        "current_level_billions": round(val, 1),
        "peak_level_billions": 2554.0,
        "drawdown_pct": round((val - 2554) / 2554 * 100, 1),
        "signal": "bullish",
        "historical": history,
        "last_updated": date.today().isoformat(),
    }


def _mock_fed_balance_sheet(days: int) -> dict:
    import random
    random.seed(88)
    data = []
    treas, mbs, total = 4200.0, 2200.0, 7500.0
    current = date.today() - timedelta(days=days)
    while current <= date.today():
        if current.weekday() < 5:
            treas += random.uniform(-8, 3)
            mbs += random.uniform(-5, 1)
            total = treas + mbs + random.uniform(800, 1200)
            data.append({
                "date": current.isoformat(),
                "treasuries": round(treas, 1),
                "mbs": round(mbs, 1),
                "other": round(total - treas - mbs, 1),
                "total": round(total, 1),
            })
        current += timedelta(days=1)
    return {
        "data": data,
        "latest": data[-1] if data else {},
        "last_updated": date.today().isoformat(),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/fed-rrp/current")
def get_fed_rrp_current(db: Session = Depends(get_db)):
    """Current Fed RRP facility level + recent history."""
    try:
        from app.models.market_indicators import MarketIndicator

        latest = (
            db.query(MarketIndicator)
            .filter(MarketIndicator.series_id == "RRPONTSYD")
            .order_by(MarketIndicator.date.desc())
            .first()
        )

        if not latest:
            return _mock_fed_rrp()

        cutoff = date.today() - timedelta(days=90)
        history = (
            db.query(MarketIndicator)
            .filter(
                MarketIndicator.series_id == "RRPONTSYD",
                MarketIndicator.date >= cutoff,
            )
            .order_by(MarketIndicator.date)
            .all()
        )

        from sqlalchemy import func
        peak_row = (
            db.query(func.max(MarketIndicator.value))
            .filter(MarketIndicator.series_id == "RRPONTSYD")
            .scalar()
        )
        peak = float(peak_row) if peak_row else float(latest.value)
        current_val = float(latest.value)
        drawdown_pct = round((current_val - peak) / peak * 100, 1) if peak > 0 else 0

        return {
            "date": latest.date.isoformat(),
            "current_level_billions": round(current_val / 1000, 1),
            "peak_level_billions": round(peak / 1000, 1),
            "drawdown_pct": drawdown_pct,
            "signal": "bullish" if current_val < peak * 0.5 else "neutral",
            "historical": [
                {"date": r.date.isoformat(), "value": round(float(r.value) / 1000, 1)}
                for r in history
            ],
            "last_updated": latest.date.isoformat(),
        }
    except Exception:
        return _mock_fed_rrp()


@router.get("/fed-balance-sheet/composition")
def get_fed_balance_sheet_composition(
    timeframe: str = Query("1Y", regex="^(1M|3M|6M|1Y|2Y|5Y|ALL)$"),
    db: Session = Depends(get_db),
):
    """Fed balance sheet breakdown: Treasuries vs MBS vs Other."""
    days = TIMEFRAME_DAYS.get(timeframe, 365)
    cutoff = date.today() - timedelta(days=days)

    try:
        from app.models.market_indicators import MarketIndicator

        treast_rows = (
            db.query(MarketIndicator)
            .filter(MarketIndicator.series_id == "TREAST", MarketIndicator.date >= cutoff)
            .order_by(MarketIndicator.date)
            .all()
        )
        mbs_rows = (
            db.query(MarketIndicator)
            .filter(MarketIndicator.series_id == "WSHOMCB", MarketIndicator.date >= cutoff)
            .order_by(MarketIndicator.date)
            .all()
        )

        if not treast_rows and not mbs_rows:
            return _mock_fed_balance_sheet(days)

        fed_rows = (
            db.query(CentralBankData)
            .filter(
                CentralBankData.source == "FED",
                CentralBankData.indicator == "balance_sheet",
                CentralBankData.date >= cutoff,
            )
            .order_by(CentralBankData.date)
            .all()
        )

        treast_map = {r.date: float(r.value) for r in treast_rows}
        mbs_map = {r.date: float(r.value) for r in mbs_rows}
        fed_map = {r.date: float(r.value) * 1000 for r in fed_rows}

        all_dates = sorted(set(treast_map.keys()) | set(mbs_map.keys()))
        data = []
        for d in all_dates:
            t = treast_map.get(d, 0) / 1000
            m = mbs_map.get(d, 0) / 1000
            total = fed_map.get(d, t + m + 1100)
            other = max(0, total - t - m)
            data.append({
                "date": d.isoformat(),
                "treasuries": round(t, 1),
                "mbs": round(m, 1),
                "other": round(other, 1),
                "total": round(total, 1),
            })

        return {
            "data": data,
            "latest": data[-1] if data else {},
            "last_updated": all_dates[-1].isoformat() if all_dates else None,
        }
    except Exception:
        return _mock_fed_balance_sheet(days)
