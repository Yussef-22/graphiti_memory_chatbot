"""Shared API schemas."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response returned by the health-check endpoint."""

    status: Literal["healthy"]
    service: str
    version: str
    environment: str


class ReadinessResponse(BaseModel):
    """Response returned after checking required infrastructure."""

    status: Literal["ready", "not_ready"]
    falkordb: Literal["healthy", "unhealthy"]
    graph: str
