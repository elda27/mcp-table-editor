from typing import Any, Sequence

from mcp.types import TextContent, Tool
from pydantic import BaseModel, create_model

from mcp_table_editor.handler.base import BaseHandler


class HandlerTool:
    def __init__(
        self,
        handler: type[BaseHandler[BaseModel, BaseModel]],
        input_args: dict[str, Any] = {},
    ) -> None:
        self.handler = handler
        self.input_args = input_args
        self.input_schema = create_model(handler.input_schema)

    def get_mcp_tool(self) -> Tool:
        """
        Get the mcp tool.
        """
        return Tool(
            name=self.handler.name,
            description=self.handler.description,
            input_schema=self.handler.input_schema.model_json_schema(),
        )

    def run(self, args: dict[str, Any]) -> Sequence[TextContent]:
        """
        Run the tool with the given input arguments.
        """
        handler_instance = self.handler(**self.input_args, **args)
        response = handler_instance.handle(self.input_args)
        return [TextContent(type="text", text=response.model_dump_json(indent=2))]
