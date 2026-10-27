from datetime import UTC, datetime

import asyncpg  # type: ignore[import-untyped]
import structlog
from fastapi import APIRouter, HTTPException, Response, status
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel
from redis.asyncio import Redis

from app.core.config import get_settings

router = APIRouter(tags=["system"])
logger = structlog.get_logger(__name__)


class HealthResponse(BaseModel):
    status: str
    service: str = "qstream-api"
    timestamp: datetime


@router.get("/health/live", response_model=HealthResponse)
async def live() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(UTC))


@router.get("/health/ready", response_model=HealthResponse)
async def ready() -> HealthResponse:
    settings = get_settings()
    database = None
    redis: Redis | None = None
    try:
        database = await asyncpg.connect(
            settings.database_url.replace("postgresql+asyncpg", "postgresql")
        )
        await database.execute("SELECT 1")
        redis = Redis.from_url(settings.redis_url)
        await redis.ping()
    except Exception as error:
        logger.warning("readiness_check_failed", dependency_error=type(error).__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="A required dependency is unavailable.",
        ) from error
    finally:
        if database is not None:
            await database.close()
        if redis is not None:
            await redis.aclose()
    return HealthResponse(status="ready", timestamp=datetime.now(UTC))


@router.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
