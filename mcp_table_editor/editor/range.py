from typing import Any, Sequence, TypeAlias

import pandas as pd

Key = Any
KeyRange = tuple[Key, Key]
AnyKeys = Key | KeyRange | Sequence[Key] | slice


class Range:
    def __init__(
        self,
        *,
        column: AnyKeys | None = None,
        row: AnyKeys | None = None,
        cell: tuple[AnyKeys, AnyKeys] | None = None,
    ) -> None:
        self.column = column
        self.row = row
        self.cell = cell

    def _get_index(self, keys: AnyKeys | None) -> pd.Index:
        if keys is None:
            return pd.Index([])
        if isinstance(keys, (list, tuple)):
            return pd.Index(keys)
        if isinstance(keys, slice):
            return pd.Index(range(keys.start, keys.stop, keys.step))
        if isinstance(keys, pd.Index):
            return keys
        return pd.Index([keys])

    def is_column_range(self) -> bool:
        return self.column is not None

    def get_columns(self) -> pd.Index:
        return self._get_index(self.column)

    def is_index_range(self) -> bool:
        return self.row is not None

    def get_index(self) -> pd.Index:
        return self._get_index(self.row)

    def is_location_range(self) -> bool:
        return self.cell is not None

    def get_location(self) -> tuple[pd.Index, pd.Index]:
        if self.cell is None:
            return pd.Index([]), pd.Index([])
        return self._get_index(self.cell[0]), self._get_index(self.cell[1])
