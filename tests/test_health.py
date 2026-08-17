"""Tests for the base API and health-check endpoint."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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

