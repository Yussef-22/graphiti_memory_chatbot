"""Liveness and readiness endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.core.config import get_settings
from app.models.schemas import HealthResponse, ReadinessResponse
from app.services.falkordb import FalkorDBService, get_falkordb_service

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Report whether the API process itself is alive."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_environment,
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={503: {"model": ReadinessResponse}},
)
async def readiness_check(
    response: Response,
    falkordb: Annotated[FalkorDBService, Depends(get_falkordb_service)],
) -> ReadinessResponse:
    """Report whether the API can reach infrastructure required for requests."""
    settings = get_settings()
    database_is_healthy = await falkordb.ping()

    if not database_is_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        status="ready" if database_is_healthy else "not_ready",
        falkordb="healthy" if database_is_healthy else "unhealthy",
        graph=settings.falkordb_graph_name,
    )
