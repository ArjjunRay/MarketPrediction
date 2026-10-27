from fastapi.testclient import TestClient

from app.main import app
from app.providers.public_data import SecEdgarProvider


def test_public_data_status_is_explicit_about_missing_price_source() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/public-data/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["market_price_source"]["source"] == "None"
    assert payload["market_price_source"]["status"] == "not_available"
    assert payload["market_price_source"]["resolution"] == "no market-price series"
    assert {source["source"] for source in payload["sources"]} == {
        "SEC EDGAR",
        "U.S. Bureau of Labor Statistics",
        "U.S. Treasury",
        "U.S. Bureau of Economic Analysis",
    }


def test_sec_endpoint_requires_operator_identity() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/public-data/sec/company/1045810/facts")

    assert response.status_code == 422
    assert "QSTREAM_SEC_USER_AGENT" in response.json()["detail"]


def test_sec_cik_normalization() -> None:
    assert SecEdgarProvider.normalize_cik("CIK1045810") == "0001045810"


def test_bea_endpoint_requires_operator_key() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/public-data/macro/bea/nipa",
            params={"table_name": "T10101", "frequency": "A", "year": "2025"},
        )

    assert response.status_code == 422
    assert "QSTREAM_BEA_API_KEY" in response.json()["detail"]
