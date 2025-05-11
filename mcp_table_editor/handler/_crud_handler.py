from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from mcp_table_editor.editor import InMemoryEditor, InsertRule, Range
from mcp_table_editor.editor._range import Range
from mcp_table_editor.handler._base_handler import BaseHandler, BaseOutputSchema


class Operation(str, Enum):
    """
    Enum for CRUD operations.
    """

    GET = "get"
    RETRIEVE = (
        "retrieve"  # alternatively, you can use "retrieve" as a synonym for "get"
    )
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    DROP = "drop"
    REMOVE = "remove"  # alternatively, you can use "remove" as a synonym for "drop"

    def __str__(self) -> str:
        return self.value


_MAPPING_OPERATION_DESCRIPTION = {
    Operation.GET: "Retrieve data from the table.",
    Operation.RETRIEVE: "Retrieve data from the table.",
    Operation.INSERT: "Insert data into the table.",
    Operation.UPDATE: "Update data in the table.",
    Operation.DELETE: "Delete data from the table.",
    Operation.DROP: "Drop data from the table.",
    Operation.REMOVE: "Drop data from the table.",
}

_OPERATION_SHAPE_CHANGES = (
    Operation.INSERT,
    Operation.UPDATE,
    Operation.DROP,
    Operation.REMOVE,
)

_OPERATION_GETTER_METHOD = (
    Operation.GET,
    Operation.RETRIEVE,
)


class CrudInputSchema(BaseModel):
    """
    Input schema for CRUD operations.
    """

    method: Operation = Field(
        ...,
        description="CRUD method to be performed.\n"
        + "\n".join(
            f"- {op}: {_MAPPING_OPERATION_DESCRIPTION[op]}"
            for op, desc in _MAPPING_OPERATION_DESCRIPTION.items()
        ),
    )
    columns: list[str] | None = Field(
        None,
        description="Column name to be used in the operation.",
    )
    rows: list[int] | None = Field(
        None,
        description="Row index to be used in the operation.",
    )
    value: Any | None = Field(
        None,
        description="Value to be used in the operation. it is used for insert and update operations.",
    )
    return_columns: list[str] | None = Field(
        None, description="Columns to be returned in the response."
    )
    insert_rule: InsertRule = Field(
        InsertRule.ABOVE,
        description="Fill rule to be used in the insert operation.",
    )
    insert_offset: int | None = Field(
        None,
        description=(
            "Offset to be used in the insert operation."
            "If int, it will be used as a row index."
            "If str, it will be used as a column name."
        ),
    )


class CrudOutputSchema(BaseOutputSchema):
    """
    Output schema for CRUD operations.
    """

    method: Operation = Field(
        ...,
        description="CRUD method to be performed.",
    )


class CrudHandler(BaseHandler[CrudInputSchema, CrudOutputSchema]):
    name: str = "Table CRUD handler"
    description: str = (
        "CRUD operations for table data.\n"
        "This handler allows you to perform CRUD operations on table data, "
        "such as inserting, updating, deleting, and retrieving data."
    )

    input_schema = CrudInputSchema
    output_schema = CrudOutputSchema

    def __init__(self, editor: InMemoryEditor, **kwargs):
        self.editor = editor

    def handle(self, args: CrudInputSchema) -> CrudOutputSchema:
        """
        Handle the CRUD operation based on the input data.
        """
        if args.columns and args.rows:
            # Create a range object based on the input data
            cell_range = Range(
                cell=(args.rows, args.columns),
            )
        elif args.columns:
            # Create a range object based on the input data
            cell_range = Range(column=args.columns)
        elif args.rows:
            # Create a range object based on the input data
            cell_range = Range(row=args.rows)
        else:
            raise ValueError("Either column or row must be provided.")

        # Perform the CRUD operation based on the method
        selector = self.editor.select(cell_range)
        if args.method in (Operation.GET, Operation.RETRIEVE):
            selector.get()
        elif args.method == Operation.INSERT:
            selector.insert(
                value=args.value, pos=args.insert_offset, insert_rule=args.insert_rule
            )
        elif args.method == Operation.UPDATE:
            selector.update(args.value)
        elif args.method == Operation.DELETE:
            selector.delete()
        elif args.method in (Operation.DROP, Operation.REMOVE):
            selector.drop()
        else:
            raise ValueError(f"Unsupported method: {args.method}")

        if args.return_columns is not None:
            # If return_columns is provided, filter the response to include only those columns
            response = selector.display_dataframe(
                args.return_columns, self.editor.index
            )
        elif args.method in _OPERATION_GETTER_METHOD:
            # If the operation changes the shape of the table, return the entire table
            response = selector.selected_dataframe()
        else:
            response = selector.display_dataframe(
                self.editor.columns, self.editor.index
            )

        return CrudOutputSchema.from_dataframe(
            response,
            method=args.method,
        )
