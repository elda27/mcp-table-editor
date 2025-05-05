from pydantic import Field

from mcp_table_editor.handler._crud_handler import (
    CrudHandler,
    CrudInputSchema,
    Operation,
)


class UpdateContentInputSchema(CrudInputSchema):
    method: Operation = Field(Operation.UPDATE)


class UpdateContentHandler(CrudHandler):
    """
    Handler for UPDATE content operations.
    """

    name = "update_content"
    description = "Update content in the table."
    input_schema = UpdateContentInputSchema
