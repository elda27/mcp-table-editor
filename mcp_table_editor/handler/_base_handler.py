import typing
from typing import Protocol, TypeVar

from pydantic import BaseModel

from mcp_table_editor.editor._editor import Editor

InputSchema = TypeVar("InputSchema", bound=BaseModel)
OutputSchema = TypeVar("OutputSchema", bound=BaseModel)


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

    def __init__(self, editor: Editor, **kwargs): ...

    def handle(self, args: InputSchema) -> OutputSchema:
        """
        Handle the request.
        """
        ...
