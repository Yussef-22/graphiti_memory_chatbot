"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api import health
from app.core.config import get_settings


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
    )
    application.include_router(health.router)

    @application.get("/", tags=["meta"])
    async def root() -> dict[str, str]:
        """Expose basic service metadata and useful documentation links."""
        return {
            "service": settings.app_name,
            "version": settings.app_version,
            "health": "/health",
            "docs": "/docs",
        }

    return application


app = create_app()

