import typing
from typing import Any, Protocol, Self, TypeVar

from pydantic import BaseModel, Field

from mcp_table_editor.editor._in_memory_editor import InMemoryEditor

InputSchema = TypeVar("InputSchema", bound=BaseModel)
OutputSchema = TypeVar("OutputSchema", bound=BaseModel)


class BaseOutputSchema(BaseModel):

    content: str | None = Field(
        None,
        description="CSV representation of the result. a result contains the selection of the table.",
    )
    json_content: list[dict[str, Any]] | None = Field(
        None,
        description="JSON representation of the result. a result contains the selection of the table.",
    )

    @classmethod
    def from_dataframe(
        cls,
        df: typing.Any,
        **kwargs,
    ) -> Self:
        """
        Create a BaseOutputSchema from a DataFrame.
        """
        return cls(
            content=df.to_csv(index=True),
            json_content=df.to_dict(orient="records"),
            **kwargs,
        )


class BaseHandler[
    InputSchema,
    OutputSchema,
](Protocol):
    """
    Base class for all handlers.
    """

    name: str
    description: str
    input_schema: type[InputSchema]
    output_schema: type[OutputSchema]

    def __init__(self, editor: InMemoryEditor, **kwargs): ...

    def handle(self, args: InputSchema) -> OutputSchema:
        """
        Handle the request.
        """
        ...
