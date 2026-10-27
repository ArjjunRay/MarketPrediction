from fastapi.testclient import TestClient

from app.main import app


def test_liveness() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_capabilities_are_honest_when_unconfigured() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/capabilities")
    payload = response.json()
    assert response.status_code == 200
    assert payload["configured"] is False
    assert payload["capabilities"] == []
    assert payload["public_display"] == []
