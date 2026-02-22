from datetime import date, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.base_models import CentralBankData, GlobalLiquidityIndex, ExchangeRate
from app.models.private_sector_liquidity import (
    EnhancedGlobalLiquidityIndex,
    PrivateSectorLiquidityIndex,
)
from app.models.capital_flows import USTreasuryTIC, BalanceOfPayments

router = APIRouter()

TIMEFRAME_DAYS = {
    "1M": 30, "3M": 90, "6M": 180, "1Y": 365,
    "2Y": 730, "5Y": 1825, "ALL": 3650,
}


def _cycle_position(change_1m: float) -> str:
    if change_1m > 1:
        return "expansion"
    if change_1m > 0:
        return "recovery"
    if change_1m > -1:
        return "slowdown"
    return "contraction"


# ---------------------------------------------------------------------------
# Mock data helpers
# ---------------------------------------------------------------------------

def _mock_gli_current() -> dict:
    return {
        "date": date.today().isoformat(),
        "value": 78.4,
        "change_pct": 0.12,
        "change_1m_pct": 1.34,
        "cycle_position": "expansion",
        "num_sources": 7,
        "cb_value": 25.9,
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
        {"source": "FED", "value": 7.5, "currency": "USD", "value_usd": 7.5, "pct_of_total": 29.0},
        {"source": "ECB", "value": 6.8, "currency": "EUR", "value_usd": 7.34, "pct_of_total": 28.4},
        {"source": "BOJ", "value": 750, "currency": "JPY", "value_usd": 5.0, "pct_of_total": 19.3},
        {"source": "BOE", "value": 0.85, "currency": "GBP", "value_usd": 1.08, "pct_of_total": 4.2},
        {"source": "SNB", "value": 0.8, "currency": "CHF", "value_usd": 0.90, "pct_of_total": 3.5},
        {"source": "BOC", "value": 0.4, "currency": "CAD", "value_usd": 0.29, "pct_of_total": 1.1},
        {"source": "RBA", "value": 0.55, "currency": "AUD", "value_usd": 0.36, "pct_of_total": 1.4},
    ]


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


def _mock_exchange_rates() -> list:
    return [
        {"currency": "AUD", "rate": 0.65, "change_pct": -0.10, "date": date.today().isoformat()},
        {"currency": "CAD", "rate": 0.74, "change_pct": 0.15, "date": date.today().isoformat()},
        {"currency": "CHF", "rate": 1.14, "change_pct": 0.05, "date": date.today().isoformat()},
        {"currency": "EUR", "rate": 1.08, "change_pct": 0.12, "date": date.today().isoformat()},
        {"currency": "GBP", "rate": 1.27, "change_pct": -0.08, "date": date.today().isoformat()},
        {"currency": "JPY", "rate": 0.00667, "change_pct": -0.22, "date": date.today().isoformat()},
    ]


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


def _mock_market_indicators_current() -> list:
    return [
        {"name": "VIX", "series_id": "VIXCLS", "value": 18.5, "change": -0.8, "signal": "neutral", "category": "volatility", "unit": "index"},
        {"name": "10Y-2Y Spread", "series_id": "T10Y2Y", "value": 0.42, "change": 0.03, "signal": "neutral", "category": "yield_curve", "unit": "percent"},
        {"name": "10Y Treasury", "series_id": "DGS10", "value": 4.25, "change": -0.02, "signal": "bearish", "category": "yield_curve", "unit": "percent"},
        {"name": "2Y Treasury", "series_id": "DGS2", "value": 3.83, "change": -0.05, "signal": "neutral", "category": "yield_curve", "unit": "percent"},
        {"name": "HY Spread", "series_id": "BAMLH0A0HYM2", "value": 3.45, "change": 0.12, "signal": "bearish", "category": "credit_spread", "unit": "percent"},
        {"name": "IG Spread", "series_id": "BAMLC0A4CBBB", "value": 1.28, "change": -0.03, "signal": "bullish", "category": "credit_spread", "unit": "percent"},
        {"name": "Breakeven Inflation", "series_id": "T10YIE", "value": 2.35, "change": 0.01, "signal": "neutral", "category": "real_rates", "unit": "percent"},
    ]


def _mock_asset_prices() -> list:
    return [
        {"asset": "S&P 500", "ticker": "SPX", "price": 5820.0, "change_pct": 0.45, "asset_class": "equity"},
        {"asset": "Gold", "ticker": "GOLD", "price": 2950.0, "change_pct": 0.22, "asset_class": "commodity"},
        {"asset": "Bitcoin", "ticker": "BTC", "price": 95000.0, "change_pct": -1.35, "asset_class": "crypto"},
    ]


def _mock_asset_correlations() -> list:
    return [
        {"asset": "S&P 500", "correlation_30d": 0.72, "correlation_90d": 0.68, "correlation_365d": 0.61, "beta_to_gli": 1.15},
        {"asset": "Gold", "correlation_30d": 0.55, "correlation_90d": 0.48, "correlation_365d": 0.42, "beta_to_gli": 0.85},
        {"asset": "Bitcoin", "correlation_30d": 0.65, "correlation_90d": 0.58, "correlation_365d": 0.52, "beta_to_gli": 1.45},
    ]


def _mock_cycle_data() -> dict:
    return {
        "current_position": "expansion",
        "momentum": 1.34,
        "cycle_day": 820,
        "total_cycle_days": 1975,
        "phase_pct": 41.5,
    }


# ---------------------------------------------------------------------------
# GLI Endpoints
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
                "num_sources": 7,
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

        # Approximate cycle position: days since earliest record / 1975 (65 months)
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


# ---------------------------------------------------------------------------
# Private Sector Endpoints
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


# ---------------------------------------------------------------------------
# Exchange Rates Endpoints
# ---------------------------------------------------------------------------

@router.get("/exchange-rates/latest")
def get_exchange_rates_latest(db: Session = Depends(get_db)):
    """Latest exchange rates for all tracked currencies."""
    try:
        latest_row = db.query(ExchangeRate.date).order_by(ExchangeRate.date.desc()).first()
        if not latest_row:
            return _mock_exchange_rates()

        latest_date = latest_row[0]
        rates = db.query(ExchangeRate).filter(ExchangeRate.date == latest_date).all()

        # Get previous business day rates for daily change
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


# ---------------------------------------------------------------------------
# Capital Flows Endpoints
# ---------------------------------------------------------------------------

@router.get("/capital-flows/tic/latest")
def get_tic_latest(db: Session = Depends(get_db)):
    """Latest US Treasury International Capital data."""
    try:
        latest = db.query(USTreasuryTIC).order_by(USTreasuryTIC.report_date.desc()).first()
    except Exception:
        return _mock_tic_latest()
    if not latest:
        return _mock_tic_latest()

    # TIC values are in millions USD from FRED; convert to trillions for display
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


# ---------------------------------------------------------------------------
# Data Refresh Endpoint
# ---------------------------------------------------------------------------

@router.post("/data/refresh")
async def refresh_data(db: Session = Depends(get_db)):
    """Trigger a data refresh for all sources."""
    try:
        from app.services.data_ingestion_service import DataIngestionService
        service = DataIngestionService(db)
        details = await service.refresh_all_data(days_back=30)
        return {
            "status": "success",
            "message": "Data refreshed successfully",
            "details": details,
            "timestamp": date.today().isoformat(),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": date.today().isoformat(),
        }


# ---------------------------------------------------------------------------
# Market Indicators Endpoints
# ---------------------------------------------------------------------------

@router.get("/market-indicators/current")
def get_market_indicators_current(db: Session = Depends(get_db)):
    """Latest values for all market indicators."""
    try:
        from app.models.market_indicators import MarketIndicator
        from sqlalchemy import func

        # Get latest date per indicator
        latest_subq = (
            db.query(
                MarketIndicator.series_id,
                func.max(MarketIndicator.date).label("max_date"),
            )
            .group_by(MarketIndicator.series_id)
            .subquery()
        )

        rows = (
            db.query(MarketIndicator)
            .join(
                latest_subq,
                (MarketIndicator.series_id == latest_subq.c.series_id)
                & (MarketIndicator.date == latest_subq.c.max_date),
            )
            .all()
        )

        if rows:
            # Also get previous day values for change calculation
            result = []
            for r in rows:
                prev = (
                    db.query(MarketIndicator)
                    .filter(
                        MarketIndicator.series_id == r.series_id,
                        MarketIndicator.date < r.date,
                    )
                    .order_by(MarketIndicator.date.desc())
                    .first()
                )
                val = float(r.value)
                prev_val = float(prev.value) if prev else val
                change = round(val - prev_val, 4)

                # Determine signal
                if r.category == "volatility":
                    signal = "bullish" if val < 15 else "bearish" if val > 25 else "neutral"
                elif r.category == "credit_spread":
                    signal = "bullish" if change < -0.05 else "bearish" if change > 0.05 else "neutral"
                elif r.category == "yield_curve":
                    if r.series_id == "T10Y2Y":
                        signal = "bullish" if val > 0.5 else "bearish" if val < 0 else "neutral"
                    else:
                        signal = "bearish" if change > 0.05 else "bullish" if change < -0.05 else "neutral"
                else:
                    signal = "neutral"

                result.append({
                    "name": r.indicator_name,
                    "series_id": r.series_id,
                    "value": round(val, 4),
                    "change": change,
                    "signal": signal,
                    "category": r.category or "other",
                    "unit": r.unit or "index",
                })
            return result
    except Exception:
        pass
    return _mock_market_indicators_current()


# ---------------------------------------------------------------------------
# Asset Prices & Correlations Endpoints
# ---------------------------------------------------------------------------

@router.get("/assets/prices")
def get_asset_prices(db: Session = Depends(get_db)):
    """Latest prices for tracked assets."""
    try:
        from app.models.asset_prices import AssetPrice
        from sqlalchemy import func

        latest_subq = (
            db.query(
                AssetPrice.asset_name,
                func.max(AssetPrice.date).label("max_date"),
            )
            .group_by(AssetPrice.asset_name)
            .subquery()
        )

        rows = (
            db.query(AssetPrice)
            .join(
                latest_subq,
                (AssetPrice.asset_name == latest_subq.c.asset_name)
                & (AssetPrice.date == latest_subq.c.max_date),
            )
            .all()
        )

        if rows:
            result = []
            for r in rows:
                prev = (
                    db.query(AssetPrice)
                    .filter(
                        AssetPrice.asset_name == r.asset_name,
                        AssetPrice.date < r.date,
                    )
                    .order_by(AssetPrice.date.desc())
                    .first()
                )
                price = float(r.price)
                prev_price = float(prev.price) if prev else price
                change_pct = round((price - prev_price) / prev_price * 100, 2) if prev_price else 0

                result.append({
                    "asset": r.asset_name,
                    "ticker": r.ticker,
                    "price": round(price, 2),
                    "change_pct": change_pct,
                    "asset_class": r.asset_class or "equity",
                })
            return result
    except Exception:
        pass
    return _mock_asset_prices()


@router.get("/assets/correlations")
def get_asset_correlations(db: Session = Depends(get_db)):
    """Asset correlations with GLI at different time windows."""
    try:
        from app.models.asset_prices import AssetCorrelation
        from sqlalchemy import func

        latest_subq = (
            db.query(
                AssetCorrelation.asset_name,
                func.max(AssetCorrelation.date).label("max_date"),
            )
            .group_by(AssetCorrelation.asset_name)
            .subquery()
        )

        rows = (
            db.query(AssetCorrelation)
            .join(
                latest_subq,
                (AssetCorrelation.asset_name == latest_subq.c.asset_name)
                & (AssetCorrelation.date == latest_subq.c.max_date),
            )
            .all()
        )

        if rows:
            return [
                {
                    "asset": r.asset_name,
                    "correlation_30d": round(float(r.correlation_30d), 4) if r.correlation_30d else 0,
                    "correlation_90d": round(float(r.correlation_90d), 4) if r.correlation_90d else 0,
                    "correlation_365d": round(float(r.correlation_365d), 4) if r.correlation_365d else 0,
                    "beta_to_gli": round(float(r.beta_to_gli), 4) if r.beta_to_gli else 0,
                }
                for r in rows
            ]
    except Exception:
        pass
    return _mock_asset_correlations()
