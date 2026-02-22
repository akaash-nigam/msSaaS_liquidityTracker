"""Capital Flows endpoints (TIC and BOP)."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.capital_flows import USTreasuryTIC, BalanceOfPayments

router = APIRouter()


def _mock_tic_latest() -> dict:
    return {
        "date": date.today().isoformat(),
        "country": "Rest of World",
        "total_holdings": 35.0,
        "treasuries": 8.0,
        "equities": 12.0,
        "corporate_bonds": 5.0,
        "agency_bonds": 2.0,
    }


def _mock_bop_latest() -> dict:
    return {
        "date": date.today().isoformat(),
        "country": "United States",
        "current_account_balance": -200.0,
        "trade_balance": -70.0,
        "financial_account_balance": -180.0,
        "net_direct_investment": -50.0,
        "net_portfolio_investment": 100.0,
    }


@router.get("/capital-flows/tic/latest")
def get_tic_latest(db: Session = Depends(get_db)):
    """Latest US Treasury International Capital data."""
    try:
        latest = db.query(USTreasuryTIC).order_by(USTreasuryTIC.report_date.desc()).first()
    except Exception:
        return _mock_tic_latest()
    if not latest:
        return _mock_tic_latest()

    def to_t(v):
        return round(float(v) / 1_000_000, 2) if v else 0

    return {
        "date": latest.report_date.isoformat(),
        "country": latest.country_name or "Rest of World",
        "total_holdings": to_t(latest.total_holdings),
        "treasuries": to_t(latest.total_treasuries),
        "equities": to_t(latest.equities),
        "corporate_bonds": to_t(latest.corporate_bonds),
        "agency_bonds": to_t(latest.agency_bonds),
    }


@router.get("/capital-flows/bop/latest")
def get_bop_latest(db: Session = Depends(get_db)):
    """Latest US Balance of Payments data."""
    try:
        latest = db.query(BalanceOfPayments).order_by(BalanceOfPayments.report_date.desc()).first()
    except Exception:
        return _mock_bop_latest()
    if not latest:
        return _mock_bop_latest()

    return {
        "date": latest.report_date.isoformat(),
        "country": latest.country_name or "United States",
        "current_account_balance": round(float(latest.current_account_balance), 2) if latest.current_account_balance else 0,
        "trade_balance": round(float(latest.trade_balance), 2) if latest.trade_balance else 0,
        "financial_account_balance": round(float(latest.financial_account_balance), 2) if latest.financial_account_balance else 0,
        "net_direct_investment": round(float(latest.net_direct_investment), 2) if latest.net_direct_investment else 0,
        "net_portfolio_investment": round(float(latest.net_portfolio_investment), 2) if latest.net_portfolio_investment else 0,
    }
