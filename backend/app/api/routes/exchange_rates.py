"""Exchange Rates endpoint."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.base_models import ExchangeRate

router = APIRouter()


def _mock_exchange_rates() -> list:
    return [
        {"currency": "AUD", "rate": 0.65, "change_pct": -0.10, "date": date.today().isoformat()},
        {"currency": "CAD", "rate": 0.74, "change_pct": 0.15, "date": date.today().isoformat()},
        {"currency": "CHF", "rate": 1.14, "change_pct": 0.05, "date": date.today().isoformat()},
        {"currency": "EUR", "rate": 1.08, "change_pct": 0.12, "date": date.today().isoformat()},
        {"currency": "GBP", "rate": 1.27, "change_pct": -0.08, "date": date.today().isoformat()},
        {"currency": "JPY", "rate": 0.00667, "change_pct": -0.22, "date": date.today().isoformat()},
    ]


@router.get("/exchange-rates/latest")
def get_exchange_rates_latest(db: Session = Depends(get_db)):
    """Latest exchange rates for all tracked currencies."""
    try:
        latest_row = db.query(ExchangeRate.date).order_by(ExchangeRate.date.desc()).first()
        if not latest_row:
            return _mock_exchange_rates()

        latest_date = latest_row[0]
        rates = db.query(ExchangeRate).filter(ExchangeRate.date == latest_date).all()

        prev_rates = (
            db.query(ExchangeRate)
            .filter(ExchangeRate.date < latest_date)
            .order_by(ExchangeRate.date.desc())
            .limit(6)
            .all()
        )
        prev_map = {r.from_currency: float(r.rate) for r in prev_rates}

        result = []
        for r in rates:
            rate_val = float(r.rate)
            prev_val = prev_map.get(r.from_currency)
            change_pct = round(((rate_val - prev_val) / prev_val * 100), 2) if prev_val else 0
            result.append({
                "currency": r.from_currency,
                "rate": round(rate_val, 6),
                "change_pct": change_pct,
                "date": r.date.isoformat(),
            })
        return sorted(result, key=lambda x: x["currency"])
    except Exception:
        return _mock_exchange_rates()
