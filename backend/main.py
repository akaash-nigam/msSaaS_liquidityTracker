from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.config import settings
from app.api.routes import router as api_router

logger = logging.getLogger("scheduler")


class CustomCORSMiddleware(BaseHTTPMiddleware):
    """Custom CORS middleware to ensure headers are properly set"""
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "")

        # Handle preflight requests
        if request.method == "OPTIONS":
            if origin in settings.ALLOWED_ORIGINS:
                response = await call_next(request)
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
                response.headers["Access-Control-Allow-Headers"] = "*"
                response.headers["Access-Control-Max-Age"] = "600"
                return response

        # Handle actual requests
        response = await call_next(request)

        if origin in settings.ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Expose-Headers"] = "*"

        return response


async def daily_ingestion():
    """Daily ingestion: exchange rates, market indicators, asset prices."""
    from app.database import SessionLocal
    from app.services.data_ingestion_service import DataIngestionService

    db = SessionLocal()
    try:
        service = DataIngestionService(db)
        result = await service.ingest_fed_data(days_back=7)
        logger.info(f"Daily ingestion complete: {result}")
    except Exception as e:
        logger.error(f"Daily ingestion failed: {e}")
    finally:
        db.close()


async def weekly_ingestion():
    """Weekly ingestion: full refresh of all data."""
    from app.database import SessionLocal
    from app.services.data_ingestion_service import DataIngestionService

    db = SessionLocal()
    try:
        service = DataIngestionService(db)
        result = await service.refresh_all_data(days_back=30)
        logger.info(f"Weekly CB + GLI ingestion: {result}")

        ps_result = await service.ingest_priority_private_sector_data(30)
        logger.info(f"Weekly PS ingestion: {ps_result}")

        await service.calculate_and_store_private_sector_index()
        await service.calculate_and_store_enhanced_gli()
        logger.info("Weekly index calculations complete")
    except Exception as e:
        logger.error(f"Weekly ingestion failed: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Global Liquidity Tracker API...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Mock data: {settings.USE_MOCK_DATA}")

    # Set up scheduler
    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        from apscheduler.triggers.cron import CronTrigger

        scheduler = AsyncIOScheduler()

        # Daily at 6am ET (11:00 UTC)
        scheduler.add_job(
            daily_ingestion,
            CronTrigger(hour=11, minute=0),
            id="daily_ingestion",
            name="Daily data ingestion",
        )

        # Weekly on Monday at 6:30am ET (11:30 UTC)
        scheduler.add_job(
            weekly_ingestion,
            CronTrigger(day_of_week="mon", hour=11, minute=30),
            id="weekly_ingestion",
            name="Weekly data ingestion",
        )

        scheduler.start()
        print(f"Scheduler started with {len(scheduler.get_jobs())} jobs")
    except ImportError:
        print("APScheduler not installed — scheduler disabled")
        scheduler = None

    yield

    # Shutdown
    if scheduler:
        scheduler.shutdown()
    print("Shutting down API...")


app = FastAPI(
    title="Global Liquidity Tracker API",
    description="API for tracking global liquidity across major central banks",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware - Using custom middleware for reliability
app.add_middleware(CustomCORSMiddleware)

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Global Liquidity Tracker API",
        "version": "2.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG
    )
