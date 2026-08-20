"""Asynchronous FalkorDB connectivity used by the API."""

import logging
from functools import lru_cache
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class FalkorDBService:
    """Own the FalkorDB client and expose small infrastructure operations."""

    def __init__(
        self,
        *,
        host: str,
        port: int,
        username: str | None,
        password: str | None,
        connect_timeout: float,
    ) -> None:
        # Imported here so unit tests can replace this service without opening
        # a real database connection or requiring Docker.
        from falkordb.asyncio import FalkorDB

        self._client: Any = FalkorDB(
            host=host,
            port=port,
            username=username,
            password=password,
            socket_connect_timeout=connect_timeout,
            socket_timeout=connect_timeout,
        )

    async def ping(self) -> bool:
        """Return True when FalkorDB answers a lightweight PING command."""
        try:
            return bool(await self._client.connection.ping())
        except Exception:
            # A readiness check should report an unavailable dependency instead
            # of crashing the endpoint or exposing connection details.
            logger.exception("FalkorDB readiness check failed")
            return False

    async def close(self) -> None:
        """Close the client's connection pool."""
        await self._client.aclose()


@lru_cache
def get_falkordb_service() -> FalkorDBService:
    """Create one reusable FalkorDB service for the application process."""
    settings = get_settings()
    return FalkorDBService(
        host=settings.falkordb_host,
        port=settings.falkordb_port,
        username=settings.falkordb_username,
        password=settings.falkordb_password,
        connect_timeout=settings.falkordb_connect_timeout,
    )
