from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class PublicDataStatus(StrEnum):
    AVAILABLE = "available"
    NEEDS_OPERATOR_CONFIGURATION = "needs_operator_configuration"
    NOT_AVAILABLE = "not_available"


class PublicSourceStatus(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str
    role: str
    status: PublicDataStatus
    api_key_required: bool
    operator_configuration: str | None
    access_method: str
    update_cadence: str
    display_delay: str
    resolution: str
    capabilities: tuple[str, ...]
    redistribution_note: str
    official_documentation: str


class PublicDataStatusResponse(BaseModel):
    market_price_source: PublicSourceStatus
    sources: tuple[PublicSourceStatus, ...]


class OfficialDataResponse(BaseModel):
    source: str
    retrieved_at: datetime
    resolution: str
    data: dict[str, object]
