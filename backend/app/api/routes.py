from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta

from app.database import get_db
from app.schemas.gli import GLIResponse, GLIHistoricalResponse, ComponentBreakdownResponse
from app.services.gli_service import GLIService

router = APIRouter()


@router.get("/gli/current", response_model=GLIResponse)
async def get_current_gli(db: Session = Depends(get_db)):
    """Get current Global Liquidity Index value"""
    service = GLIService(db)
    gli = await service.get_current_gli()

    if not gli:
        raise HTTPException(status_code=404, detail="No GLI data available")

    return gli


@router.get("/gli/historical", response_model=GLIHistoricalResponse)
async def get_historical_gli(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    timeframe: str = "1Y",
    db: Session = Depends(get_db)
):
    """
    Get historical GLI data

    Parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - timeframe: Predefined timeframe (1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y, ALL)
    """
    service = GLIService(db)

    # Parse dates or use timeframe
    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        # Calculate dates from timeframe
        end = date.today()
        timeframe_map = {
            "1M": 30,
            "3M": 90,
            "6M": 180,
            "1Y": 365,
            "3Y": 1095,
            "5Y": 1825,
            "10Y": 3650,
            "ALL": 10000  # Large number for all data
        }
        days = timeframe_map.get(timeframe, 365)
        start = end - timedelta(days=days)

    historical_data = await service.get_historical_gli(start, end)

    return {
        "start_date": start,
        "end_date": end,
        "data_points": len(historical_data),
        "data": historical_data
    }


@router.get("/gli/components", response_model=ComponentBreakdownResponse)
async def get_component_breakdown(
    date_str: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get component breakdown for GLI calculation

    Parameters:
    - date: Date for breakdown (YYYY-MM-DD), defaults to latest
    """
    service = GLIService(db)

    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        target_date = date.today()

    components = await service.get_component_breakdown(target_date)

    return {
        "date": target_date,
        "components": components,
        "total_gli": sum(c["value"] for c in components)
    }


@router.get("/gli/cycle")
async def get_cycle_info(db: Session = Depends(get_db)):
    """Get liquidity cycle information"""
    service = GLIService(db)
    cycle_info = await service.get_cycle_info()

    return cycle_info


@router.post("/data/refresh")
async def refresh_data(db: Session = Depends(get_db)):
    """Trigger data refresh from external sources"""
    # This would be called by a scheduled job
    from app.services.data_ingestion_service import DataIngestionService

    service = DataIngestionService(db)
    results = await service.refresh_all_data()

    return {
        "status": "success",
        "results": results,
        "timestamp": datetime.now()
    }
