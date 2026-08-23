"""API tests for temporal memory and chat endpoints."""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.memory import (
    ChatResult,
    MemoryFactRecord,
    MemoryServiceUnavailableError,
    MemoryWriteResult,
    get_memory_service,
)

client = TestClient(app)

FACT = MemoryFactRecord(
    uuid="fact-1",
    fact="Yussef practica natación.",
    valid_at=datetime(2026, 8, 23, tzinfo=timezone.utc),
    invalid_at=None,
)


class FakeMemoryService:
    """Test double that never contacts Gemini or FalkorDB."""

    async def add_memory(self, **_) -> MemoryWriteResult:
        return MemoryWriteResult(
            graph="graphiti_memory_yussef",
            episode_uuid="episode-1",
            facts_extracted=1,
        )

    async def search(self, **_) -> tuple[str, list[MemoryFactRecord]]:
        return "graphiti_memory_yussef", [FACT]

    async def chat(self, **_) -> ChatResult:
        return ChatResult(
            graph="graphiti_memory_yussef",
            answer="Podrías hacer una sesión ligera de natación.",
            memories=[FACT],
            episode_uuid="episode-2",
        )


class UnavailableMemoryService(FakeMemoryService):
    """Test double used to verify safe provider error mapping."""

    async def search(self, **_):
        raise MemoryServiceUnavailableError("Servicio temporalmente no disponible.")


@pytest.fixture(autouse=True)
def override_memory_service():
    app.dependency_overrides[get_memory_service] = FakeMemoryService
    yield
    app.dependency_overrides.clear()


def test_add_memory_episode_returns_created_result() -> None:
    response = client.post(
        "/memory/episodes",
        json={"user_id": "yussef", "content": "Practico natación."},
    )

    assert response.status_code == 201
    assert response.json() == {
        "user_id": "yussef",
        "graph": "graphiti_memory_yussef",
        "episode_uuid": "episode-1",
        "facts_extracted": 1,
    }


def test_search_memory_returns_ranked_temporal_facts() -> None:
    response = client.post(
        "/memory/search",
        json={"user_id": "yussef", "query": "¿Qué deporte practico?", "limit": 5},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["graph"] == "graphiti_memory_yussef"
    assert body["facts"][0]["fact"] == "Yussef practica natación."
    assert body["facts"][0]["invalid_at"] is None


def test_chat_returns_answer_and_memory_transparency() -> None:
    response = client.post(
        "/chat",
        json={"user_id": "yussef", "message": "¿Qué actividad puedo hacer hoy?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["memory_saved"] is True
    assert body["episode_uuid"] == "episode-2"
    assert body["memories_used"][0]["uuid"] == "fact-1"
    assert "natación" in body["answer"]


def test_invalid_user_id_is_rejected_before_reaching_services() -> None:
    response = client.post(
        "/memory/search",
        json={"user_id": "../../another-user", "query": "secreto"},
    )

    assert response.status_code == 422


def test_provider_failures_are_returned_as_safe_503_errors() -> None:
    app.dependency_overrides[get_memory_service] = UnavailableMemoryService

    response = client.post(
        "/memory/search",
        json={"user_id": "yussef", "query": "¿Qué recuerdas?"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Servicio temporalmente no disponible."}
