from datetime import UTC, datetime
from typing import Any
from xml.etree import ElementTree

import httpx

from app.providers.base import FundamentalDataProvider, MacroDataProvider
from app.schemas.public_data import OfficialDataResponse


class UpstreamDataError(RuntimeError):
    """An official upstream source did not return usable data."""


class SecEdgarProvider(FundamentalDataProvider):
    base_url = "https://data.sec.gov"

    def __init__(self, user_agent: str, timeout_seconds: float = 15.0) -> None:
        self._user_agent = user_agent.strip()
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    @property
    def configured(self) -> bool:
        return bool(self._user_agent)

    async def _get(self, path: str) -> dict[str, object]:
        if not self.configured:
            raise UpstreamDataError(
                "SEC access requires QSTREAM_SEC_USER_AGENT with an operator name and email."
            )
        response = await self._client.get(
            f"{self.base_url}{path}",
            headers={"User-Agent": self._user_agent, "Accept-Encoding": "gzip, deflate"},
        )
        response.raise_for_status()
        payload: Any = response.json()
        if not isinstance(payload, dict):
            raise UpstreamDataError("SEC returned an unexpected response shape.")
        return payload

    @staticmethod
    def normalize_cik(cik: str) -> str:
        digits = cik.strip().removeprefix("CIK").lstrip("0") or "0"
        if not digits.isdigit() or len(digits) > 10:
            raise ValueError("CIK must contain at most 10 digits.")
        return digits.zfill(10)

    async def company_facts(self, cik: str) -> dict[str, object]:
        return await self._get(f"/api/xbrl/companyfacts/CIK{self.normalize_cik(cik)}.json")

    async def company_submissions(self, cik: str) -> dict[str, object]:
        return await self._get(f"/submissions/CIK{self.normalize_cik(cik)}.json")

    async def close(self) -> None:
        await self._client.aclose()


class BlsPublicDataProvider(MacroDataProvider):
    endpoint = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    def __init__(self, timeout_seconds: float = 15.0) -> None:
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    async def series(
        self, series_ids: tuple[str, ...], start_year: int | None, end_year: int | None
    ) -> dict[str, object]:
        if not series_ids or len(series_ids) > 25:
            raise ValueError("BLS public requests require between 1 and 25 series IDs.")
        payload: dict[str, object] = {"seriesid": list(series_ids)}
        if start_year is not None:
            payload["startyear"] = str(start_year)
        if end_year is not None:
            payload["endyear"] = str(end_year)
        response = await self._client.post(self.endpoint, json=payload)
        response.raise_for_status()
        data: Any = response.json()
        if not isinstance(data, dict):
            raise UpstreamDataError("BLS returned an unexpected response shape.")
        return data

    async def close(self) -> None:
        await self._client.aclose()


class BeaPublicDataProvider:
    endpoint = "https://apps.bea.gov/api/data"

    def __init__(self, api_key: str, timeout_seconds: float = 30.0) -> None:
        self._api_key = api_key.strip()
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    @property
    def configured(self) -> bool:
        return bool(self._api_key)

    async def nipa_series(self, table_name: str, frequency: str, year: str) -> dict[str, object]:
        if not self.configured:
            raise UpstreamDataError("BEA access requires an operator-owned QSTREAM_BEA_API_KEY.")
        response = await self._client.get(
            self.endpoint,
            params={
                "UserID": self._api_key,
                "method": "GetData",
                "datasetname": "NIPA",
                "TableName": table_name,
                "Frequency": frequency,
                "Year": year,
                "ResultFormat": "JSON",
            },
        )
        response.raise_for_status()
        data: Any = response.json()
        if not isinstance(data, dict):
            raise UpstreamDataError("BEA returned an unexpected response shape.")
        return data

    async def close(self) -> None:
        await self._client.aclose()


class TreasuryYieldProvider:
    endpoint = (
        "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"
    )

    def __init__(self, timeout_seconds: float = 15.0) -> None:
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    async def yields(self, year: int) -> OfficialDataResponse:
        response = await self._client.get(
            self.endpoint,
            params={"data": "daily_treasury_yield_curve", "field_tdr_date_value": year},
        )
        response.raise_for_status()
        try:
            root = ElementTree.fromstring(response.content)
        except ElementTree.ParseError as exc:
            raise UpstreamDataError("Treasury returned invalid XML.") from exc

        records: list[dict[str, object]] = []
        for properties in root.findall(
            ".//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties"
        ):
            record: dict[str, object] = {}
            for field in properties:
                name = field.tag.rsplit("}", 1)[-1]
                record[name] = field.text
            records.append(record)
        return OfficialDataResponse(
            source="U.S. Treasury",
            retrieved_at=datetime.now(UTC),
            resolution="daily",
            data={"year": year, "observations": records},
        )

    async def close(self) -> None:
        await self._client.aclose()
