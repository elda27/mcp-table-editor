from pydantic import Field

from mcp_table_editor.handler._crud_handler import (
    CrudHandler,
    CrudInputSchema,
    Operation,
)


class RemoveContentInputSchema(CrudInputSchema):
    method: Operation = Field(Operation.REMOVE)


class RemoveContentHandler(CrudHandler):
    """
    Handler for REMOVE content operations.
    """

    name = "remove_content"
    description = "Remove content from the table."
    input_schema = RemoveContentInputSchema
