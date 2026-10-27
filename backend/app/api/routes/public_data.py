from datetime import UTC, datetime
from typing import Annotated

import httpx
from fastapi import APIRouter, HTTPException, Query, Request

from app.providers.public_data import (
    BeaPublicDataProvider,
    BlsPublicDataProvider,
    SecEdgarProvider,
    TreasuryYieldProvider,
    UpstreamDataError,
)
from app.schemas.public_data import (
    OfficialDataResponse,
    PublicDataStatus,
    PublicDataStatusResponse,
    PublicSourceStatus,
)

router = APIRouter(prefix="/api/v1/public-data", tags=["public data"])


def _sources(sec_configured: bool, bea_configured: bool) -> PublicDataStatusResponse:
    market = PublicSourceStatus(
        source="None",
        role="US equity and ETF prices",
        status=PublicDataStatus.NOT_AVAILABLE,
        api_key_required=False,
        operator_configuration=None,
        access_method="disabled",
        update_cadence="not applicable",
        display_delay="not applicable",
        resolution="no market-price series",
        capabilities=(),
        redistribution_note=(
            "No verified zero-cost source currently grants anonymous public price redistribution."
        ),
        official_documentation="/docs/providers",
    )
    return PublicDataStatusResponse(
        market_price_source=market,
        sources=(
            PublicSourceStatus(
                source="SEC EDGAR",
                role="company facts and filing events",
                status=(
                    PublicDataStatus.AVAILABLE
                    if sec_configured
                    else PublicDataStatus.NEEDS_OPERATOR_CONFIGURATION
                ),
                api_key_required=False,
                operator_configuration="QSTREAM_SEC_USER_AGENT (operator name and email)",
                access_method="HTTPS JSON API",
                update_cadence="near real time as filings are disseminated",
                display_delay="none stated; subject to SEC publication timing",
                resolution="filing/event",
                capabilities=("company_facts", "submissions", "filing_events"),
                redistribution_note="Public records; cite SEC as the source.",
                official_documentation=(
                    "https://www.sec.gov/search-filings/edgar-application-programming-interfaces"
                ),
            ),
            PublicSourceStatus(
                source="U.S. Bureau of Labor Statistics",
                role="economic time series",
                status=PublicDataStatus.AVAILABLE,
                api_key_required=False,
                operator_configuration=None,
                access_method="HTTPS JSON API v2, unregistered limits",
                update_cadence="per official release schedule",
                display_delay="none beyond official release timing",
                resolution="series-dependent, commonly monthly",
                capabilities=("economic_series",),
                redistribution_note="BLS-authored data is public domain; preserve source labels.",
                official_documentation="https://www.bls.gov/developers/api_faqs.htm",
            ),
            PublicSourceStatus(
                source="U.S. Treasury",
                role="daily Treasury par yield curve rates",
                status=PublicDataStatus.AVAILABLE,
                api_key_required=False,
                operator_configuration=None,
                access_method="HTTPS XML feed",
                update_cadence="daily on business days",
                display_delay="none beyond official publication timing",
                resolution="daily",
                capabilities=("treasury_yield_curve",),
                redistribution_note="Official U.S. government source; preserve source labels.",
                official_documentation=(
                    "https://home.treasury.gov/treasury-daily-interest-rate-xml-feed"
                ),
            ),
            PublicSourceStatus(
                source="U.S. Bureau of Economic Analysis",
                role="national and industry economic accounts",
                status=(
                    PublicDataStatus.AVAILABLE
                    if bea_configured
                    else PublicDataStatus.NEEDS_OPERATOR_CONFIGURATION
                ),
                api_key_required=True,
                operator_configuration="QSTREAM_BEA_API_KEY (free operator registration)",
                access_method="HTTPS JSON API",
                update_cadence="per official release schedule",
                display_delay="none beyond official release timing",
                resolution="series-dependent, quarterly or annual",
                capabilities=("nipa_series", "gdp", "industry_accounts"),
                redistribution_note="Published BEA statistics are public domain; cite BEA.",
                official_documentation="https://apps.bea.gov/api/signup/",
            ),
        ),
    )


@router.get("/status", response_model=PublicDataStatusResponse)
async def status(request: Request) -> PublicDataStatusResponse:
    provider: SecEdgarProvider = request.app.state.sec_provider
    bea_provider: BeaPublicDataProvider = request.app.state.bea_provider
    return _sources(provider.configured, bea_provider.configured)


def _upstream_error(exc: Exception) -> HTTPException:
    if isinstance(exc, (ValueError, UpstreamDataError)):
        return HTTPException(status_code=422, detail=str(exc))
    if isinstance(exc, httpx.HTTPStatusError):
        return HTTPException(
            status_code=502,
            detail=f"Official upstream source returned HTTP {exc.response.status_code}.",
        )
    return HTTPException(status_code=503, detail="Official upstream source is unavailable.")


@router.get("/sec/company/{cik}/facts", response_model=OfficialDataResponse)
async def sec_company_facts(cik: str, request: Request) -> OfficialDataResponse:
    provider: SecEdgarProvider = request.app.state.sec_provider
    try:
        data = await provider.company_facts(cik)
    except (ValueError, UpstreamDataError, httpx.HTTPError) as exc:
        raise _upstream_error(exc) from exc
    return OfficialDataResponse(
        source="SEC EDGAR",
        retrieved_at=datetime.now(UTC),
        resolution="filing/event",
        data=data,
    )


@router.get("/sec/company/{cik}/submissions", response_model=OfficialDataResponse)
async def sec_company_submissions(cik: str, request: Request) -> OfficialDataResponse:
    provider: SecEdgarProvider = request.app.state.sec_provider
    try:
        data = await provider.company_submissions(cik)
    except (ValueError, UpstreamDataError, httpx.HTTPError) as exc:
        raise _upstream_error(exc) from exc
    return OfficialDataResponse(
        source="SEC EDGAR",
        retrieved_at=datetime.now(UTC),
        resolution="filing/event",
        data=data,
    )


@router.get("/macro/bls", response_model=OfficialDataResponse)
async def bls_series(
    request: Request,
    series_id: Annotated[list[str], Query(min_length=1, max_length=25)],
    start_year: Annotated[int | None, Query(ge=1913, le=2100)] = None,
    end_year: Annotated[int | None, Query(ge=1913, le=2100)] = None,
) -> OfficialDataResponse:
    provider: BlsPublicDataProvider = request.app.state.bls_provider
    try:
        data = await provider.series(tuple(series_id), start_year, end_year)
    except (ValueError, UpstreamDataError, httpx.HTTPError) as exc:
        raise _upstream_error(exc) from exc
    return OfficialDataResponse(
        source="U.S. Bureau of Labor Statistics",
        retrieved_at=datetime.now(UTC),
        resolution="series-dependent",
        data=data,
    )


@router.get("/macro/treasury/yields", response_model=OfficialDataResponse)
async def treasury_yields(
    request: Request, year: Annotated[int, Query(ge=1990, le=2100)]
) -> OfficialDataResponse:
    provider: TreasuryYieldProvider = request.app.state.treasury_provider
    try:
        return await provider.yields(year)
    except (UpstreamDataError, httpx.HTTPError) as exc:
        raise _upstream_error(exc) from exc


@router.get("/macro/bea/nipa", response_model=OfficialDataResponse)
async def bea_nipa_series(
    request: Request,
    table_name: Annotated[str, Query(pattern=r"^[A-Za-z0-9]+$", max_length=32)],
    frequency: Annotated[str, Query(pattern=r"^[AQM]$")],
    year: Annotated[str, Query(pattern=r"^(X|\d{4})(,(X|\d{4}))*$", max_length=64)],
) -> OfficialDataResponse:
    provider: BeaPublicDataProvider = request.app.state.bea_provider
    try:
        data = await provider.nipa_series(table_name, frequency, year)
    except (UpstreamDataError, httpx.HTTPError) as exc:
        raise _upstream_error(exc) from exc
    return OfficialDataResponse(
        source="U.S. Bureau of Economic Analysis",
        retrieved_at=datetime.now(UTC),
        resolution="series-dependent",
        data=data,
    )
