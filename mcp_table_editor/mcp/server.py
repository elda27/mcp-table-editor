from contextlib import asynccontextmanager
from logging import basicConfig, getLogger
from typing import AsyncIterator

import mcp
import mcp.server.stdio

# import mcp.server.fastmcp
# from fastmcp import FastMCP
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import TextContent, Tool

from mcp_table_editor._version import __version__
from mcp_table_editor.editor import InMemoryEditor
from mcp_table_editor.handler import TOOL_HANDLERS
from mcp_table_editor.mcp.handler_tool import HandlerTool

basicConfig(
    level="INFO",
)
_logger = getLogger(__name__)

TOOLS: dict[str, HandlerTool] = {
    handler.name: HandlerTool(handler) for handler in TOOL_HANDLERS  #  type: ignore
}


@asynccontextmanager
async def editor_context(server: Server) -> AsyncIterator[InMemoryEditor]:
    editor = InMemoryEditor()
    yield editor


app: Server = Server("mcp-table-editor", __version__, lifespan=editor_context)
# app: mcp.server.fastmcp.FastMCP = mcp.server.fastmcp.FastMCP(
#     "mcp-table-editor", __version__, lifespan=editor_context
# )


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all tools.
    """
    return [tool.get_mcp_tool() for tool in TOOLS.values()]


@app.call_tool()
async def call_tool(name: str, args: dict) -> list[TextContent]:
    """
    Call a tool with the given name and arguments.
    """
    editor: InMemoryEditor = app.request_context.lifespan_context
    if name not in TOOLS:
        raise ValueError(f"Tool {name} not found.")
    _logger.info(f"Calling tool: {name} with args: {args}")
    tool = TOOLS[name]
    return tool.run(editor, args)


async def run_server():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-table-editor",
                server_version=__version__,
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
            raise_exceptions=True,
        )


if __name__ == "__main__":
    import asyncio

    _logger.info("Starting MCP Table Editor server...")
    # asyncio.run(run())
    asyncio.run(run_server())
