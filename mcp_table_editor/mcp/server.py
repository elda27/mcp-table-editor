from mcp.server import Server

from mcp_table_editor._version import __version__
from mcp_table_editor.mcp.handler_tool import HandlerTool

app = Server("mcp-table-editor", __version__)

TOOLS: dict[str, HandlerTool] = {""}
