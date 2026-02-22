"""Data management endpoints (refresh, freshness)."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.base_models import GlobalLiquidityIndex, ExchangeRate
from app.models.private_sector_liquidity import PrivateSectorLiquidityIndex
from app.models.capital_flows import USTreasuryTIC

router = APIRouter()


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


@router.get("/data/freshness")
def get_data_freshness(db: Session = Depends(get_db)):
    """Return last_updated timestamps for all data categories."""
    from sqlalchemy import func

    def max_date(model, date_col=None):
        try:
            col = date_col or model.date
            result = db.query(func.max(col)).scalar()
            return result.isoformat() if result else None
        except Exception:
            return None

    try:
        from app.models.market_indicators import MarketIndicator
        from app.models.asset_prices import AssetPrice
        from app.models.liquidity_valuation import LiquidityValuation

        return {
            "gli": max_date(GlobalLiquidityIndex),
            "private_sector": max_date(PrivateSectorLiquidityIndex),
            "exchange_rates": max_date(ExchangeRate),
            "market_indicators": max_date(MarketIndicator),
            "asset_prices": max_date(AssetPrice),
            "capital_flows": max_date(USTreasuryTIC, USTreasuryTIC.report_date),
            "valuations": max_date(LiquidityValuation),
        }
    except Exception:
        return {
            "gli": None,
            "private_sector": None,
            "exchange_rates": None,
            "market_indicators": None,
            "asset_prices": None,
            "capital_flows": None,
            "valuations": None,
        }
