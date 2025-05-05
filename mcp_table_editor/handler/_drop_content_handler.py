from pydantic import Field

from mcp_table_editor.handler._crud_handler import (
    CrudHandler,
    CrudInputSchema,
    Operation,
)


class DropContentInputSchema(CrudInputSchema):
    method: Operation = Field(Operation.DROP)


class DropContentHandler(CrudHandler):
    """
    Handler for DROP content operations.
    """

    name = "drop_content"
    description = "Drop content from the table."
    input_schema = DropContentInputSchema
