from enum import Enum
from typing import Any, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from mcp_table_editor.editor.editor import Editor
from mcp_table_editor.editor.range import Range
from mcp_table_editor.handler.base import BaseHandler


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
    column: list[str] | None = Field(
        None,
        description="Column name to be used in the operation.",
    )
    row: list[int] | None = Field(
        None,
        description="Row index to be used in the operation.",
    )
    value: str | None = Field(
        None,
        description="Value to be used in the operation. it is used for insert and update operations.",
    )
    insert_rule: Literal["above", "empty"] = Field(
        "above",
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


class CrudOutputSchema(BaseModel):
    """
    Output schema for CRUD operations.
    """

    method: Operation = Field(
        ...,
        description="CRUD method to be performed.",
    )

    response: Any = Field(
        None,
        description="Result of the operation.",
    )
    json_content: dict[str, Any] | None = Field(
        None,
        description="JSON representation of the result.",
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

    def __init__(self, editor: Editor, operation: Operation, **kwargs):
        self.editor = editor
        self.operation = operation

    def handle(self, args: CrudInputSchema) -> CrudOutputSchema:
        """
        Handle the CRUD operation based on the input data.
        """
        if args.column and args.row:
            # Create a range object based on the input data
            cell_range = Range(
                cell=(args.row, args.column),
            )
        elif args.column:
            # Create a range object based on the input data
            cell_range = Range(cell=(self.editor.index, args.column))
        elif args.row:
            # Create a range object based on the input data
            cell_range = Range(cell=(args.row, self.editor.columns))
        else:
            raise ValueError("Either column or row must be provided.")

        # Perform the CRUD operation based on the method
        selector = self.editor.select(cell_range)
        if args.method in (Operation.GET, Operation.RETRIEVE):
            response = selector.get()
        elif args.method == Operation.INSERT:
            response = selector.insert(
                args.value, pos=args.insert_offset, insert_rule=args.insert_rule
            )
        elif args.method == Operation.UPDATE:
            response = selector.update(args.value)
        elif args.method == Operation.DELETE:
            response = selector.delete()
        elif args.method in (Operation.DROP, Operation.REMOVE):
            response = selector.drop()
        else:
            raise ValueError(f"Unsupported method: {args.method}")

        return CrudOutputSchema(
            method=args.method,
            response=response.to_csv(),
            json_content=response.to_dict(orient="records"),
        )
