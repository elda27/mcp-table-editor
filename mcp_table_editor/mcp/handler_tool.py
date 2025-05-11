from typing import Any, Sequence

from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field, create_model

from mcp_table_editor.editor import InMemoryEditor
from mcp_table_editor.handler._base_handler import BaseHandler


class HandlerTool:
    def __init__(
        self,
        handler: type[BaseHandler[BaseModel, BaseModel]],
    ) -> None:
        self.handler = handler

    @property
    def name(self) -> str:
        """
        Get the name of the handler.
        """
        return self.handler.name

    def get_mcp_tool(self) -> Tool:
        """
        Get the mcp tool.
        """
        return Tool(
            name=self.handler.name,
            description=self.handler.description,
            inputSchema=self.handler.input_schema.model_json_schema(),
        )

    def run(
        self, editor: InMemoryEditor, args: dict[str, Any]
    ) -> Sequence[TextContent]:
        """
        Run the tool with the given input arguments.
        """
        handler_instance = self.handler(editor)
        response = handler_instance.handle(**args)
        return [TextContent(type="text", text=response.model_dump_json(indent=2))]
