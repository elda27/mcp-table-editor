from typing import Any, Sequence

from pydantic import BaseModel, Field

from mcp_table_editor.editor import InMemoryEditor
from mcp_table_editor.handler._base_handler import BaseHandler, BaseOutputSchema


class SortByValueInputSchema(BaseModel):
    """
    Input model for the SortHandler.
    """

    by: list[str] = Field(
        default=...,
        description="The column(s) to sort by.",
    )
    values: list[list[Any]] = Field(
        default=...,
        description="The values to sort by. Each sublist corresponds to a column in 'by'.",
    )


SortByValueOutputSchema = BaseOutputSchema


class SortByValueHandler(BaseHandler[SortByValueInputSchema, SortByValueOutputSchema]):
    """
    Handler for sorting a table.
    """

    name: str = "sort_by_value"
    input_schema: type[SortByValueInputSchema] = SortByValueInputSchema
    output_schema: type[SortByValueOutputSchema] = SortByValueOutputSchema
    description: str = (
        "Sort the table by the specified column(s) and order(s). "
        "The order is determined by the values provided."
    )

    def __init__(self, editor: InMemoryEditor) -> None:
        self.editor = editor

    def handle(self, args: SortByValueInputSchema) -> SortByValueOutputSchema:
        """
        Handle the sort operation.

        Parameters
        ----------
        args : SortInputSchema
            The arguments for the sort operation.

        Returns
        -------
        SortOutputSchema
            The result of the sort operation.
        """
        self.editor.sort_by_values(args.by, values=args.values)
        df = self.editor.get_table()
        return SortByValueOutputSchema.from_dataframe(df)
