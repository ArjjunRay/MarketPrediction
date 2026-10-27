from typing import Annotated

from fastapi import APIRouter, Query

from app.schemas.instruments import InstrumentSearchResponse
from app.services.instruments import InstrumentSearchService

router = APIRouter(prefix="/api/v1/instruments", tags=["instruments"])
service = InstrumentSearchService()


@router.get("/search", response_model=InstrumentSearchResponse)
async def search_instruments(
    q: Annotated[str, Query(max_length=100)] = "",
    limit: Annotated[int, Query(ge=1, le=25)] = 10,
) -> InstrumentSearchResponse:
    return InstrumentSearchResponse(query=q, results=service.search(q, limit))
