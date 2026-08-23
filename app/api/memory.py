"""Endpoints for adding and retrieving temporal memories."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import (
    AddMemoryRequest,
    AddMemoryResponse,
    MemoryFact,
    SearchMemoryRequest,
    SearchMemoryResponse,
)
from app.services.memory import (
    GraphitiMemoryService,
    MemoryFactRecord,
    MemoryServiceError,
    get_memory_service,
)

router = APIRouter(prefix="/memory", tags=["memory"])


def _fact_response(record: MemoryFactRecord) -> MemoryFact:
    return MemoryFact(
        uuid=record.uuid,
        fact=record.fact,
        valid_at=record.valid_at,
        invalid_at=record.invalid_at,
    )


@router.post(
    "/episodes",
    response_model=AddMemoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_memory_episode(
    request: AddMemoryRequest,
    service: Annotated[GraphitiMemoryService, Depends(get_memory_service)],
) -> AddMemoryResponse:
    """Turn one user statement into temporal graph memory."""
    try:
        result = await service.add_memory(
            user_id=request.user_id,
            content=request.content,
            reference_time=request.reference_time,
        )
    except MemoryServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return AddMemoryResponse(
        user_id=request.user_id,
        graph=result.graph,
        episode_uuid=result.episode_uuid,
        facts_extracted=result.facts_extracted,
    )


@router.post("/search", response_model=SearchMemoryResponse)
async def search_memory(
    request: SearchMemoryRequest,
    service: Annotated[GraphitiMemoryService, Depends(get_memory_service)],
) -> SearchMemoryResponse:
    """Search only inside the requesting user's graph namespace."""
    try:
        graph, records = await service.search(
            user_id=request.user_id,
            query=request.query,
            limit=request.limit,
        )
    except MemoryServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return SearchMemoryResponse(
        user_id=request.user_id,
        graph=graph,
        query=request.query,
        facts=[_fact_response(record) for record in records],
    )
