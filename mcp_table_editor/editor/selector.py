from enum import Enum
from typing import Any

import pandas as pd

from mcp_table_editor.editor.config import EditorConfig
from mcp_table_editor.editor.range import Range


class InsertRule(str, Enum):
    """
    Enum for insert rules.
    """

    ABOVE = "above"  # Fill above the selected cell
    EMPTY = "empty"  # Fill empty cells in the selected range

    def __str__(self) -> str:
        return self.value


class Selector:
    def __init__(
        self, df: pd.DataFrame, cell_range: Range, editor_config: EditorConfig
    ) -> None:
        self.df = df
        self.range = cell_range
        self.editor_config = editor_config

    def drop(self) -> pd.DataFrame:
        df = self.df
        if self.range.is_column_range():
            df.drop(columns=self.range.get_columns(), inplace=True)
        if self.range.is_index_range():
            df.drop(index=self.range.get_index(), inplace=True)
        if self.range.is_location_range():
            df.drop(columns=self.range.cell, inplace=True)
        return df

    def _get_range(self, range: Range) -> pd.DataFrame:
        df = self.df
        if self.range.is_column_range():
            return df[range.get_columns()]
        if self.range.is_index_range():
            return df.loc[range.get_index()]
        if self.range.is_location_range():
            index, columns = range.get_location()
            return df.loc[index, columns]
        raise KeyError("Invalid range")

    def _set_value(self, range: Range, value: Any) -> pd.DataFrame:
        df = self.df
        if range.is_column_range():
            df[range.get_columns()] = value
        if range.is_index_range():
            df.loc[range.get_index()] = value
        if range.is_location_range():
            index, columns = self.range.get_location()
            df.loc[index, columns] = value
        return df

    def delete(self) -> pd.DataFrame:
        return self._set_value(self.range, pd.NA)

    def get(self) -> pd.DataFrame:
        return self._get_range(self.range)

    def update(self, value: Any) -> pd.DataFrame:
        return self._set_value(self.range, value)

    def insert(
        self,
        pos: int | str | None = None,
        value: Any = pd.NA,
        insert_rule: InsertRule = InsertRule.ABOVE,
    ) -> pd.DataFrame:
        df = self.df
        if self.range.is_column_range():
            cols = self.range.get_columns()
            df = df.insert(pos or len(df.columns), cols)
        if self.range.is_index_range():
            index = self.range.get_index()
            df = pd.concat(
                [df, pd.DataFrame(value, index=index, columns=df.columns)],
                axis=0,
            )
        if self.range.is_location_range():
            index, columns = self.range.get_location()
            df = df.insert(pos or len(df), columns, value)
            df = pd.concat(
                [df, pd.DataFrame(value, index=index, columns=df.columns)],
                axis=0,
            )
        if insert_rule == InsertRule.ABOVE:
            df = df.ffill(axis=0)
        return df
