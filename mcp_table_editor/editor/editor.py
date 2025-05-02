from typing import Any, Iterable, Protocol, Sequence, TypeVar

import pandas as pd
from ulid import ulid

from mcp_table_editor.editor.config import EditorConfig
from mcp_table_editor.editor.range import Range
from mcp_table_editor.editor.selector import Selector


class Editor:
    def __init__(
        self,
        table: pd.DataFrame | None = None,
        config: EditorConfig | None = None,
    ) -> None:
        self.id = ulid()
        if table is None:
            table = pd.DataFrame()
        else:
            self.table = table
        self.schema: dict[str, str] = {}
        self.config = config or EditorConfig.default()

    def select(self, range: Range) -> Selector:
        return Selector(self.table, range, self.config)

    def select_all(self) -> Selector:
        """
        Select all cells in the table.
        """
        return self.select(Range(row=self.table.index, column=self.table.columns))

    @property
    def columns(self) -> pd.Index:
        # Get the columns of the table.
        # TODO: If the table has too many columns, we should return a subset of the columns.
        # Note that it is controlled by the config.
        return self.table.columns

    @property
    def index(self) -> pd.Index:
        # Get the rows of the table.
        # TODO: If the table has too many rows, we should return a subset of the rows.
        # Note that it is controlled by the config.
        return self.table.index
