from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Capability(StrEnum):
    TRADES = "trades"
    BARS = "bars"
    NBBO = "nbbo"
    L2 = "l2"
    L3_MBO = "l3_mbo"
    NEWS = "news"


class AccessMode(StrEnum):
    PUBLIC = "public"
    RESEARCH = "research"


class ProviderCapabilities(BaseModel):
    model_config = ConfigDict(frozen=True)

    provider: str
    configured: bool
    simulated: bool
    capabilities: frozenset[Capability]
    public_display: frozenset[Capability]
    notes: tuple[str, ...] = ()
