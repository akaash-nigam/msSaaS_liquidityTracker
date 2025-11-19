from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.config import settings
from app.api.routes import router as api_router


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Global Liquidity Tracker API...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    yield
    # Shutdown
    print("👋 Shutting down API...")


app = FastAPI(
    title="Global Liquidity Tracker API",
    description="API for tracking global liquidity across major central banks",
    version="1.0.0",
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
        "version": "1.0.0",
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
