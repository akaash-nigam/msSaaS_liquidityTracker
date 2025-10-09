from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from decimal import Decimal

from app.models.global_liquidity_index import GlobalLiquidityIndex
from app.models.central_bank_data import CentralBankData


class GLIService:
    """Service for Global Liquidity Index operations"""

    def __init__(self, db: Session):
        self.db = db

    async def get_current_gli(self) -> Optional[Dict[str, Any]]:
        """Get the most recent GLI entry"""
        gli = self.db.query(GlobalLiquidityIndex).order_by(
            desc(GlobalLiquidityIndex.date)
        ).first()

        if not gli:
            # Return mock data if no real data exists
            return {
                "date": date.today(),
                "value": 176.2,
                "change_pct": 0.2,
                "change_1m_pct": 2.4,
                "change_3m_pct": 5.1,
                "change_6m_pct": 6.3,
                "change_1y_pct": 7.8,
                "cycle_position": "expansion"
            }

        return {
            "date": gli.date,
            "value": float(gli.value),
            "change_pct": float(gli.change_pct) if gli.change_pct else None,
            "change_1m_pct": float(gli.change_1m_pct) if gli.change_1m_pct else None,
            "change_3m_pct": float(gli.change_3m_pct) if gli.change_3m_pct else None,
            "change_6m_pct": float(gli.change_6m_pct) if gli.change_6m_pct else None,
            "change_1y_pct": float(gli.change_1y_pct) if gli.change_1y_pct else None,
            "cycle_position": gli.cycle_position
        }

    async def get_historical_gli(
        self,
        start_date: date,
        end_date: date
    ) -> List[Dict[str, Any]]:
        """Get historical GLI data within date range"""
        results = self.db.query(GlobalLiquidityIndex).filter(
            GlobalLiquidityIndex.date >= start_date,
            GlobalLiquidityIndex.date <= end_date
        ).order_by(GlobalLiquidityIndex.date).all()

        if not results:
            # Return mock data for demonstration
            import random
            from datetime import timedelta
            mock_data = []
            current_date = start_date
            base_value = 150.0

            while current_date <= end_date:
                days_since_start = (current_date - start_date).days
                trend = days_since_start * 0.05
                variation = random.uniform(-2, 2)
                value = base_value + trend + variation

                mock_data.append({
                    "date": current_date,
                    "value": round(value, 2)
                })
                current_date += timedelta(days=7)  # Weekly data

            return mock_data

        return [
            {
                "date": record.date,
                "value": float(record.value)
            }
            for record in results
        ]

    async def get_component_breakdown(self, target_date: date) -> List[Dict[str, Any]]:
        """Get breakdown of GLI components for a specific date"""

        # Mock data for now - will be replaced with real central bank data
        components = [
            {
                "source": "FED",
                "name": "Federal Reserve (Net)",
                "value": 6.8,
                "change_1m": 0.12,
                "percent_of_total": 38.6,
                "trend": "up"
            },
            {
                "source": "PBOC",
                "name": "People's Bank of China",
                "value": 5.2,
                "change_1m": 0.085,
                "percent_of_total": 29.5,
                "trend": "up"
            },
            {
                "source": "ECB",
                "name": "European Central Bank",
                "value": 3.1,
                "change_1m": -0.02,
                "percent_of_total": 17.6,
                "trend": "down"
            },
            {
                "source": "BOJ",
                "name": "Bank of Japan",
                "value": 1.9,
                "change_1m": 0.015,
                "percent_of_total": 10.8,
                "trend": "up"
            },
            {
                "source": "BOE",
                "name": "Bank of England",
                "value": 0.8,
                "change_1m": 0.005,
                "percent_of_total": 4.5,
                "trend": "up"
            },
        ]

        return components

    async def get_cycle_info(self) -> Dict[str, Any]:
        """Get liquidity cycle information"""
        return {
            "current_day": 1842,
            "total_days": 1950,
            "phase": "Late Expansion",
            "days_to_peak": 108,
            "projected_peak_date": "2025-09-15",
            "last_trough": "2022-12-01",
            "last_peak": "2021-06-15"
        }
