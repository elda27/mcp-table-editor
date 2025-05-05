from pydantic import Field

from mcp_table_editor.handler._crud_handler import (
    CrudHandler,
    CrudInputSchema,
    Operation,
)


class GetContentInputSchema(CrudInputSchema):
    method: Operation = Field(Operation.GET)


class GetContentHandler(CrudHandler):
    """
    Handler for GET content operations.
    """

    name = "get_content"
    description = "Get content from the table."
    input_schema = GetContentInputSchema
