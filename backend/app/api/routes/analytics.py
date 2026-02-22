"""Analytics endpoints: cycle allocation, world map, correlation matrix, sankey, multi-timeframe."""

from datetime import date, timedelta
import random

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from .helpers import TIMEFRAME_DAYS, _cycle_position

router = APIRouter()


# ---------------------------------------------------------------------------
# Phase C: Cycle-Based Asset Allocation
# ---------------------------------------------------------------------------

ALLOCATION_MAP = {
    "expansion":   [("Equities", 50, "Risk-on phase favors equities with strong momentum"),
                    ("Bonds", 15, "Low allocation as yields rise during expansion"),
                    ("Gold", 10, "Minimal hedge needed in expansion"),
                    ("Crypto", 15, "High-beta assets benefit from liquidity surge"),
                    ("Cash", 10, "Minimal cash drag during growth")],
    "slowdown":    [("Equities", 25, "Reduce equity exposure as momentum fades"),
                    ("Bonds", 35, "Duration gains as rates peak and turn"),
                    ("Gold", 20, "Safe haven allocation increases"),
                    ("Crypto", 5, "Reduce high-beta exposure"),
                    ("Cash", 15, "Raise cash for opportunities ahead")],
    "contraction": [("Equities", 10, "Minimal equity exposure during deleveraging"),
                    ("Bonds", 40, "Maximum duration bet as rates fall"),
                    ("Gold", 30, "Peak safe haven demand"),
                    ("Crypto", 0, "Zero allocation in risk-off environment"),
                    ("Cash", 20, "Maximum dry powder for recovery")],
    "recovery":    [("Equities", 40, "Re-risk as cycle turns positive"),
                    ("Bonds", 20, "Reduce duration as yields bottom"),
                    ("Gold", 15, "Maintain moderate hedge"),
                    ("Crypto", 10, "Early cycle crypto re-entry"),
                    ("Cash", 15, "Deploying cash into risk assets")],
}

ASSET_COLORS = {
    "Equities": "#3b82f6",
    "Bonds": "#8b5cf6",
    "Gold": "#f59e0b",
    "Crypto": "#a78bfa",
    "Cash": "#64748b",
}


@router.get("/analytics/cycle-allocation")
def get_cycle_allocation(db: Session = Depends(get_db)):
    """Cycle-based asset allocation using Howell framework."""
    try:
        from app.models.private_sector_liquidity import EnhancedGlobalLiquidityIndex
        from app.models.base_models import GlobalLiquidityIndex

        latest = db.query(EnhancedGlobalLiquidityIndex).order_by(EnhancedGlobalLiquidityIndex.date.desc()).first()
        if not latest:
            latest = db.query(GlobalLiquidityIndex).order_by(GlobalLiquidityIndex.date.desc()).first()

        if latest:
            change_1m = float(latest.change_1m_pct) if latest.change_1m_pct else 0
            position = _cycle_position(change_1m)
            momentum = round(change_1m, 2)
        else:
            position = "expansion"
            momentum = 1.34
    except Exception:
        position = "expansion"
        momentum = 1.34

    allocs = ALLOCATION_MAP.get(position, ALLOCATION_MAP["expansion"])
    return {
        "cycle_position": position,
        "momentum": momentum,
        "allocations": [
            {
                "asset_class": name,
                "weight": weight,
                "rationale": rationale,
                "color": ASSET_COLORS.get(name, "#64748b"),
            }
            for name, weight, rationale in allocs
        ],
    }


# ---------------------------------------------------------------------------
# Phase E: World Map
# ---------------------------------------------------------------------------

@router.get("/analytics/world-map")
def get_world_map_data(db: Session = Depends(get_db)):
    """Country-level liquidity data for world map visualization."""
    # CB balance sheets mapped to ISO Alpha-3 codes
    cb_map = {
        "FED": ("USA", "United States"),
        "ECB": ("DEU", "Eurozone"),
        "BOJ": ("JPN", "Japan"),
        "BOE": ("GBR", "United Kingdom"),
        "SNB": ("CHE", "Switzerland"),
        "RBA": ("AUS", "Australia"),
        "BOC": ("CAN", "Canada"),
        "PBOC": ("CHN", "China"),
    }

    try:
        from app.models.base_models import CentralBankData, GlobalLiquidityIndex, ExchangeRate

        latest_gli = db.query(GlobalLiquidityIndex).order_by(GlobalLiquidityIndex.date.desc()).first()
        if latest_gli:
            d = latest_gli.date
            banks = db.query(CentralBankData).filter(
                CentralBankData.date == d,
                CentralBankData.indicator == "balance_sheet",
            ).all()

            if banks:
                total_usd = 0
                entries = []
                for b in banks:
                    val_usd = float(b.value)
                    if b.currency != "USD":
                        fx = db.query(ExchangeRate).filter(
                            ExchangeRate.from_currency == b.currency,
                            ExchangeRate.date == d,
                        ).first()
                        if fx:
                            val_usd = float(b.value) * float(fx.rate)
                    total_usd += val_usd
                    entries.append((b.source, val_usd))

                result = []
                for source, val_usd in entries:
                    if source in cb_map:
                        code, name = cb_map[source]
                        result.append({
                            "country_code": code,
                            "country": name,
                            "cb_assets_usd": round(val_usd, 2),
                            "buffett_ratio": None,
                            "signal": "neutral",
                            "liquidity_contribution_pct": round(val_usd / total_usd * 100, 1) if total_usd else 0,
                        })
                return result
    except Exception:
        pass

    # Mock fallback
    mock_data = [
        {"country_code": "USA", "country": "United States", "cb_assets_usd": 7.5, "buffett_ratio": 209.0, "signal": "extreme", "liquidity_contribution_pct": 22.9},
        {"country_code": "DEU", "country": "Eurozone", "cb_assets_usd": 7.34, "buffett_ratio": 52.0, "signal": "fair", "liquidity_contribution_pct": 22.4},
        {"country_code": "CHN", "country": "China", "cb_assets_usd": 6.80, "buffett_ratio": 65.0, "signal": "fair", "liquidity_contribution_pct": 20.8},
        {"country_code": "JPN", "country": "Japan", "cb_assets_usd": 5.0, "buffett_ratio": 148.0, "signal": "elevated", "liquidity_contribution_pct": 15.3},
        {"country_code": "GBR", "country": "United Kingdom", "cb_assets_usd": 1.08, "buffett_ratio": 105.0, "signal": "elevated", "liquidity_contribution_pct": 3.3},
        {"country_code": "CHE", "country": "Switzerland", "cb_assets_usd": 0.90, "buffett_ratio": None, "signal": "neutral", "liquidity_contribution_pct": 2.8},
        {"country_code": "AUS", "country": "Australia", "cb_assets_usd": 0.36, "buffett_ratio": None, "signal": "neutral", "liquidity_contribution_pct": 1.1},
        {"country_code": "CAN", "country": "Canada", "cb_assets_usd": 0.29, "buffett_ratio": 140.0, "signal": "elevated", "liquidity_contribution_pct": 0.9},
    ]
    return mock_data


# ---------------------------------------------------------------------------
# Phase F: Correlation Matrix
# ---------------------------------------------------------------------------

@router.get("/analytics/correlation-matrix")
def get_correlation_matrix(db: Session = Depends(get_db)):
    """NxN correlation matrix for GLI, SPX, Gold, BTC, VIX, DXY, US10Y."""
    labels = ["GLI", "SPX", "Gold", "BTC", "VIX", "DXY", "US10Y"]

    # Realistic mock correlation matrix
    matrix = [
        [ 1.00,  0.68,  0.45,  0.58, -0.42, -0.55,  0.12],  # GLI
        [ 0.68,  1.00,  0.15,  0.52, -0.75, -0.30,  0.05],  # SPX
        [ 0.45,  0.15,  1.00,  0.32, -0.10, -0.65,  0.20],  # Gold
        [ 0.58,  0.52,  0.32,  1.00, -0.35, -0.25,  0.08],  # BTC
        [-0.42, -0.75, -0.10, -0.35,  1.00,  0.15, -0.18],  # VIX
        [-0.55, -0.30, -0.65, -0.25,  0.15,  1.00, -0.10],  # DXY
        [ 0.12,  0.05,  0.20,  0.08, -0.18, -0.10,  1.00],  # US10Y
    ]

    return {"labels": labels, "matrix": matrix}


# ---------------------------------------------------------------------------
# Phase G: Sankey Flow Diagram
# ---------------------------------------------------------------------------

@router.get("/analytics/sankey-flows")
def get_sankey_flows(db: Session = Depends(get_db)):
    """Liquidity flow data for Sankey diagram: CB Sources -> Channels -> Destinations."""
    nodes = [
        # Sources (left column)
        {"id": "fed", "name": "Federal Reserve", "category": "source"},
        {"id": "ecb", "name": "ECB", "category": "source"},
        {"id": "boj", "name": "Bank of Japan", "category": "source"},
        {"id": "pboc", "name": "PBOC", "category": "source"},
        {"id": "other_cb", "name": "Other CBs", "category": "source"},
        # Channels (middle column)
        {"id": "qe_qt", "name": "QE / QT", "category": "channel"},
        {"id": "private_credit", "name": "Private Credit", "category": "channel"},
        {"id": "stablecoins", "name": "Stablecoins", "category": "channel"},
        # Destinations (right column)
        {"id": "equities", "name": "Equities", "category": "destination"},
        {"id": "bonds", "name": "Bonds", "category": "destination"},
        {"id": "gold", "name": "Gold", "category": "destination"},
        {"id": "crypto", "name": "Crypto", "category": "destination"},
        {"id": "real_estate", "name": "Real Estate", "category": "destination"},
    ]

    links = [
        # Sources -> Channels
        {"source": "fed", "target": "qe_qt", "value": 4500},
        {"source": "fed", "target": "private_credit", "value": 2000},
        {"source": "ecb", "target": "qe_qt", "value": 3800},
        {"source": "ecb", "target": "private_credit", "value": 1500},
        {"source": "boj", "target": "qe_qt", "value": 3200},
        {"source": "pboc", "target": "qe_qt", "value": 2800},
        {"source": "pboc", "target": "private_credit", "value": 3500},
        {"source": "other_cb", "target": "qe_qt", "value": 1200},
        {"source": "other_cb", "target": "stablecoins", "value": 200},
        # Channels -> Destinations
        {"source": "qe_qt", "target": "equities", "value": 6000},
        {"source": "qe_qt", "target": "bonds", "value": 5500},
        {"source": "qe_qt", "target": "gold", "value": 2000},
        {"source": "qe_qt", "target": "real_estate", "value": 2000},
        {"source": "private_credit", "target": "equities", "value": 3000},
        {"source": "private_credit", "target": "bonds", "value": 2000},
        {"source": "private_credit", "target": "real_estate", "value": 2000},
        {"source": "stablecoins", "target": "crypto", "value": 150},
        {"source": "stablecoins", "target": "equities", "value": 50},
    ]

    return {"nodes": nodes, "links": links}


# ---------------------------------------------------------------------------
# Phase H: Multi-Timeframe Dashboard
# ---------------------------------------------------------------------------

@router.get("/analytics/multi-timeframe")
def get_multi_timeframe(db: Session = Depends(get_db)):
    """GLI at three timeframes: 1M, 1Y, 5Y."""
    timeframes = [("1M", 30), ("1Y", 365), ("5Y", 1825)]

    try:
        from app.models.private_sector_liquidity import EnhancedGlobalLiquidityIndex
        from app.models.base_models import GlobalLiquidityIndex

        panels = []
        for label, days in timeframes:
            cutoff = date.today() - timedelta(days=days)
            rows = (
                db.query(EnhancedGlobalLiquidityIndex)
                .filter(EnhancedGlobalLiquidityIndex.date >= cutoff)
                .order_by(EnhancedGlobalLiquidityIndex.date)
                .all()
            )
            if not rows:
                rows = (
                    db.query(GlobalLiquidityIndex)
                    .filter(GlobalLiquidityIndex.date >= cutoff)
                    .order_by(GlobalLiquidityIndex.date)
                    .all()
                )

            if rows:
                values = []
                for r in rows:
                    v = float(r.total_value) if hasattr(r, "total_value") else float(r.value)
                    values.append(v)

                gli_data = [
                    {"date": r.date.isoformat(), "value": round(float(r.total_value) if hasattr(r, "total_value") else float(r.value), 2)}
                    for r in rows
                ]
                current = values[-1]
                first = values[0]
                change_pct = round((current - first) / first * 100, 2) if first else 0

                panels.append({
                    "timeframe": label,
                    "gli_data": gli_data,
                    "change_pct": change_pct,
                    "high": round(max(values), 2),
                    "low": round(min(values), 2),
                    "current": round(current, 2),
                })
            else:
                panels.append(_mock_timeframe_panel(label, days))

        if panels:
            return {"panels": panels}
    except Exception:
        pass

    return {
        "panels": [
            _mock_timeframe_panel("1M", 30),
            _mock_timeframe_panel("1Y", 365),
            _mock_timeframe_panel("5Y", 1825),
        ]
    }


def _mock_timeframe_panel(label: str, days: int) -> dict:
    random.seed(hash(label))
    points = []
    value = 80.0 if days > 365 else 83.0
    current = date.today() - timedelta(days=days)
    values = []
    while current <= date.today():
        if current.weekday() < 5:
            value += random.uniform(-0.2, 0.25)
            points.append({"date": current.isoformat(), "value": round(value, 2)})
            values.append(value)
        current += timedelta(days=1)
    current_val = values[-1] if values else 85.0
    first_val = values[0] if values else 80.0
    return {
        "timeframe": label,
        "gli_data": points,
        "change_pct": round((current_val - first_val) / first_val * 100, 2) if first_val else 0,
        "high": round(max(values), 2) if values else 86.0,
        "low": round(min(values), 2) if values else 78.0,
        "current": round(current_val, 2),
    }
