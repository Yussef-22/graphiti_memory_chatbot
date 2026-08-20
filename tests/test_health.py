"""Tests for the base API and health-check endpoint."""

from fastapi.testclient import TestClient
import pytest

from app.services.falkordb import get_falkordb_service
from app.main import app

client = TestClient(app)


class FakeFalkorDBService:
    """Small test double that avoids requiring Docker in unit tests."""

    def __init__(self, *, healthy: bool) -> None:
        self.healthy = healthy

    async def ping(self) -> bool:
        return self.healthy


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    """Keep dependency replacements isolated between tests."""
    yield
    app.dependency_overrides.clear()


def test_root_returns_service_metadata() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "Graphiti Memory Chatbot"
    assert response.json()["docs"] == "/docs"


def test_health_check_returns_healthy_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "Graphiti Memory Chatbot",
        "version": "0.1.0",
        "environment": "development",
    }


def test_readiness_returns_ready_when_falkordb_is_available() -> None:
    app.dependency_overrides[get_falkordb_service] = lambda: FakeFalkorDBService(
        healthy=True
    )

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "falkordb": "healthy",
        "graph": "graphiti_memory",
    }


def test_readiness_returns_503_when_falkordb_is_unavailable() -> None:
    app.dependency_overrides[get_falkordb_service] = lambda: FakeFalkorDBService(
        healthy=False
    )

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "falkordb": "unhealthy",
        "graph": "graphiti_memory",
    }
