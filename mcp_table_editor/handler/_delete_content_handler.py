from pydantic import Field

from mcp_table_editor.handler._crud_handler import (
    CrudHandler,
    CrudInputSchema,
    Operation,
)


class DeleteContentInputSchema(CrudInputSchema):
    method: Operation = Field(Operation.DELETE)


class DeleteContentHandler(CrudHandler):
    """
    Handler for DELETE content operations.
    """

    name = "delete_content"
    description = "Delete content from the table."
    input_schema = DeleteContentInputSchema
