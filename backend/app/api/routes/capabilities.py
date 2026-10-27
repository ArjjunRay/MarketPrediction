from typing import cast

from fastapi import APIRouter, Request

from app.schemas.capabilities import ProviderCapabilities

router = APIRouter(prefix="/api/v1", tags=["capabilities"])


@router.get("/capabilities", response_model=ProviderCapabilities)
async def capabilities(request: Request) -> ProviderCapabilities:
    return cast(ProviderCapabilities, request.app.state.market_provider.capabilities)
