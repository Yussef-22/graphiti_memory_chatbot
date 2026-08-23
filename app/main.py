"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import chat, health, memory
from app.core.config import get_settings
from app.services.falkordb import get_falkordb_service
from app.services.memory import get_memory_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Release cached database clients when the application stops."""
    yield

    if get_memory_service.cache_info().currsize:
        await get_memory_service().close()
        get_memory_service.cache_clear()

    if get_falkordb_service.cache_info().currsize:
        await get_falkordb_service().close()
        get_falkordb_service.cache_clear()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Chatbot API with persistent temporal memory powered by "
            "Graphiti and FalkorDB."
        ),
        lifespan=lifespan,
    )
    application.include_router(health.router)
    application.include_router(memory.router)
    application.include_router(chat.router)

    @application.get("/", tags=["meta"])
    async def root() -> dict[str, str]:
        """Expose basic service metadata and useful documentation links."""
        return {
            "service": settings.app_name,
            "version": settings.app_version,
            "health": "/health",
            "readiness": "/ready",
            "chat": "/chat",
            "memory": "/memory/search",
            "docs": "/docs",
        }

    return application


app = create_app()
