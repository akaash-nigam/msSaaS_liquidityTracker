"""Routes package — aggregates all sub-routers into a single `router`."""

from fastapi import APIRouter

from .gli import router as gli_router
from .private_sector import router as ps_router
from .fed import router as fed_router
from .exchange_rates import router as fx_router
from .capital_flows import router as cf_router
from .liquidity_flows import router as lf_router
from .market import router as market_router
from .data import router as data_router
from .analytics import router as analytics_router
from .stablecoins import router as stablecoin_router

router = APIRouter()
router.include_router(gli_router)
router.include_router(ps_router)
router.include_router(fed_router)
router.include_router(fx_router)
router.include_router(cf_router)
router.include_router(lf_router)
router.include_router(market_router)
router.include_router(data_router)
router.include_router(analytics_router)
router.include_router(stablecoin_router)
