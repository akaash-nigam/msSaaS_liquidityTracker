from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from decimal import Decimal


class GLIDataPoint(BaseModel):
    date: date
    value: float

    class Config:
        from_attributes = True


class GLIResponse(BaseModel):
    date: date
    value: float
    change_pct: Optional[float] = None
    change_1m_pct: Optional[float] = None
    change_3m_pct: Optional[float] = None
    change_6m_pct: Optional[float] = None
    change_1y_pct: Optional[float] = None
    cycle_position: Optional[str] = None

    class Config:
        from_attributes = True


class GLIHistoricalResponse(BaseModel):
    start_date: date
    end_date: date
    data_points: int
    data: List[GLIDataPoint]


class ComponentData(BaseModel):
    source: str
    name: str
    value: float
    change_1m: Optional[float] = None
    percent_of_total: Optional[float] = None
    trend: Optional[str] = None


class ComponentBreakdownResponse(BaseModel):
    date: date
    components: List[ComponentData]
    total_gli: float
