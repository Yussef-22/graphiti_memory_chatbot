"""Shared API schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    """Base model that trims surrounding whitespace from text inputs."""

    model_config = ConfigDict(str_strip_whitespace=True)


class HealthResponse(APIModel):
    """Response returned by the health-check endpoint."""

    status: Literal["healthy"]
    service: str
    version: str
    environment: str


class ReadinessResponse(APIModel):
    """Response returned after checking required infrastructure."""

    status: Literal["ready", "not_ready"]
    falkordb: Literal["healthy", "unhealthy"]
    graph: str


class UserScopedRequest(APIModel):
    """Base request whose user id is safe to use as a graph namespace."""

    user_id: str = Field(
        min_length=1,
        max_length=48,
        pattern=r"^[A-Za-z0-9_-]+$",
        examples=["yussef"],
        description="Stable user id containing letters, numbers, dashes or underscores.",
    )


class MemoryFact(APIModel):
    """One temporal fact retrieved from the user's knowledge graph."""

    uuid: str
    fact: str
    valid_at: datetime | None = None
    invalid_at: datetime | None = None


class AddMemoryRequest(UserScopedRequest):
    """A user statement that Graphiti should turn into graph memory."""

    content: str = Field(min_length=1, max_length=4000, examples=["Me gusta nadar."])
    reference_time: datetime | None = Field(
        default=None,
        description="When the statement was true; current UTC time when omitted.",
    )


class AddMemoryResponse(APIModel):
    """Result of ingesting one memory episode."""

    user_id: str
    graph: str
    episode_uuid: str
    facts_extracted: int


class SearchMemoryRequest(UserScopedRequest):
    """Semantic question used to retrieve a user's memories."""

    query: str = Field(min_length=1, max_length=1000, examples=["¿Qué deporte practico?"])
    limit: int = Field(default=5, ge=1, le=20)


class SearchMemoryResponse(APIModel):
    """Temporal facts ranked for a memory query."""

    user_id: str
    graph: str
    query: str
    facts: list[MemoryFact]


class ChatRequest(UserScopedRequest):
    """A chat message whose relevant memories should be retrieved first."""

    message: str = Field(
        min_length=1,
        max_length=4000,
        examples=["¿Qué actividad me recomendarías para hoy?"],
    )
    reference_time: datetime | None = Field(
        default=None,
        description="When this message occurred; current UTC time when omitted.",
    )


class ChatResponse(APIModel):
    """Assistant answer plus transparent memory metadata."""

    user_id: str
    graph: str
    answer: str
    memories_used: list[MemoryFact]
    memory_saved: bool
    episode_uuid: str
