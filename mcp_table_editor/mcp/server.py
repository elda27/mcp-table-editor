from contextlib import asynccontextmanager
from typing import AsyncIterator

import mcp
import mcp.server.stdio
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import TextContent, Tool

from mcp_table_editor._version import __version__
from mcp_table_editor.editor import Editor
from mcp_table_editor.handler import TOOL_HANDLERS
from mcp_table_editor.mcp.handler_tool import HandlerTool

TOOLS: dict[str, HandlerTool] = {
    handler.name: HandlerTool(handler) for handler in TOOL_HANDLERS  #  type: ignore
}


@asynccontextmanager
async def editor_context() -> AsyncIterator[Editor]:
    editor = Editor()
    yield editor


app: Server = Server("mcp-table-editor", __version__, lifespan=editor_context)


@app.list_tools()
def list_tools() -> dict[str, Tool]:
    """
    List all tools.
    """
    return {name: tool.get_mcp_tool() for name, tool in TOOLS.items()}


@app.call_tool()
def call_tool(name: str, args: dict) -> list[TextContent]:
    """
    Call a tool with the given name and arguments.
    """
    editor: Editor = app.request_context.lifespan_context
    if name not in TOOLS:
        raise ValueError(f"Tool {name} not found.")
    tool = TOOLS[name]
    return tool.run(editor, args)


async def run():
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
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
