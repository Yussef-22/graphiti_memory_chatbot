"""Memory-aware chatbot endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import ChatRequest, ChatResponse, MemoryFact
from app.services.memory import (
    GraphitiMemoryService,
    MemoryServiceError,
    get_memory_service,
)

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: Annotated[GraphitiMemoryService, Depends(get_memory_service)],
) -> ChatResponse:
    """Answer using relevant prior memories, then store the user's message."""
    try:
        result = await service.chat(
            user_id=request.user_id,
            message=request.message,
            reference_time=request.reference_time,
        )
    except MemoryServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return ChatResponse(
        user_id=request.user_id,
        graph=result.graph,
        answer=result.answer,
        memories_used=[
            MemoryFact(
                uuid=memory.uuid,
                fact=memory.fact,
                valid_at=memory.valid_at,
                invalid_at=memory.invalid_at,
            )
            for memory in result.memories
        ],
        memory_saved=True,
        episode_uuid=result.episode_uuid,
    )
