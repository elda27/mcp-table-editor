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
        self.table = table or pd.DataFrame()
        self.schema: dict[str, str] = {}
        self.config = config or EditorConfig.default()

    def select(self, range: Range) -> Selector:
        return Selector(self.table, range, self.config)

    @property
    def columns(self) -> pd.Index:
        return self.table.columns

    @property
    def index(self) -> pd.Index:
        return self.table.index
