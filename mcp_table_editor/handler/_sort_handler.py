from typing import Any, Sequence

from pydantic import BaseModel, Field

from mcp_table_editor.editor import InMemoryEditor
from mcp_table_editor.handler._base_handler import BaseHandler, BaseOutputSchema


class SortInputSchema(BaseModel):
    """
    Input model for the SortHandler.
    """

    by: Sequence[str] = Field(
        default=...,
        description="The column(s) to sort by. If None, sort by all columns.",
    )
    ascending: bool = Field(
        default=True,
        description="Whether to sort in ascending order. If False, sort in descending order.",
    )


SortOutputSchema = BaseOutputSchema


class SortHandler(BaseHandler[SortInputSchema, SortOutputSchema]):
    """
    Handler for sorting a table.
    """

    name: str = "sort"
    input_schema: type[SortInputSchema] = SortInputSchema
    output_schema: type[SortOutputSchema] = SortOutputSchema
    description: str = (
        "Sort the table by the specified column(s). If no column is specified, sort by all columns."
    )

    def __init__(self, editor: InMemoryEditor) -> None:
        self.editor = editor

    def handle(self, args: SortInputSchema) -> SortOutputSchema:
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
        self.editor.sort(by=args.by, ascending=args.ascending)
        df = self.editor.get_table()
        return SortOutputSchema.from_dataframe(df)
