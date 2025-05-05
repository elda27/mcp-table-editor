from pydantic import Field

from mcp_table_editor.handler._crud_handler import (
    CrudHandler,
    CrudInputSchema,
    Operation,
)


class InsertCellInputSchema(CrudInputSchema):
    method: Operation = Field(Operation.INSERT)


class InsertContentHandler(CrudHandler):
    """
    Handler for INSERT cell operations.
    """

    name = "insert_cell"
    description = "Insert a cell into the table."
    input_schema = InsertCellInputSchema
