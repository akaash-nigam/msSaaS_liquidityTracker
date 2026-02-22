"""Market Indicators and Asset Prices/Correlations endpoints."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter()


# ---------------------------------------------------------------------------
# Mock data helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/market-indicators/current")
def get_market_indicators_current(db: Session = Depends(get_db)):
    """Latest values for all market indicators."""
    try:
        from app.models.market_indicators import MarketIndicator
        from sqlalchemy import func

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
