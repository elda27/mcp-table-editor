import contextlib
from logging import basicConfig, getLogger
from typing import AsyncIterator

from fastapi import FastAPI
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

from mcp_table_editor.mcp.config import McpSettings
from mcp_table_editor.mcp.event_store import InMemoryEventStore
from mcp_table_editor.mcp.server import app as mcp_app

basicConfig(
    level="INFO",
)
_logger = getLogger(__name__)

event_store = InMemoryEventStore()
settings = McpSettings()

# Create the session manager with our app and event store
session_manager = StreamableHTTPSessionManager(
    app=mcp_app,
    event_store=event_store,  # Enable resumability
    json_response=settings.json_response,
)


async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
    await session_manager.handle_request(scope, receive, send)


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    """Context manager for managing session manager lifecycle."""
    async with session_manager.run():
        _logger.info("Application started with StreamableHTTP session manager!")
        try:
            yield
        finally:
            _logger.info("Application shutting down...")


# Create an ASGI application using the transport
app = FastAPI(
    debug=settings.debug,
    routes=[
        Mount("/mcp", app=handle_streamable_http),
    ],
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Welcome to the MCP Table Editor! Visit /mcp for the MCP API."}


@app.get("/table/{id}")
async def get_table(id: str):
    """Get a table by its ID."""
    table = event_store.get_table(id)
    if table:
        return table
    else:
        return {"error": "Table not found"}, 404


if __name__ == "__main__":
    import uvicorn

    # Run the app using Uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
