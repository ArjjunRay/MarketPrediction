from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import perf_counter

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from app.api.router import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.monitoring.metrics import HTTP_LATENCY, HTTP_REQUESTS
from app.providers.public_data import (
    BeaPublicDataProvider,
    BlsPublicDataProvider,
    SecEdgarProvider,
    TreasuryYieldProvider,
)
from app.providers.simulated import SimulatedMarketDataProvider

settings = get_settings()
configure_logging(settings.log_level)
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.market_provider = SimulatedMarketDataProvider(
        enabled=settings.enable_simulated_provider
    )
    app.state.sec_provider = SecEdgarProvider(
        user_agent=settings.sec_user_agent,
        timeout_seconds=settings.public_data_timeout_seconds,
    )
    app.state.bls_provider = BlsPublicDataProvider(settings.public_data_timeout_seconds)
    app.state.bea_provider = BeaPublicDataProvider(
        settings.bea_api_key, settings.public_data_timeout_seconds
    )
    app.state.treasury_provider = TreasuryYieldProvider(settings.public_data_timeout_seconds)
    logger.info(
        "application_started",
        environment=settings.env,
        simulated_provider_enabled=settings.enable_simulated_provider,
    )
    yield
    await app.state.market_provider.close()
    await app.state.sec_provider.close()
    await app.state.bls_provider.close()
    await app.state.bea_provider.close()
    await app.state.treasury_provider.close()
    logger.info("application_stopped")


app = FastAPI(
    title="QStream API",
    version="0.1.0",
    description="Provider-neutral market intelligence API foundation",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def observe_request(request: Request, call_next: RequestResponseEndpoint) -> Response:
    started = perf_counter()
    response = await call_next(request)
    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    HTTP_REQUESTS.labels(request.method, path, response.status_code).inc()
    HTTP_LATENCY.labels(request.method, path).observe(perf_counter() - started)
    return response


app.include_router(router)
