from typing import Any, Iterable, Protocol, Sequence, TypeVar

import pandas as pd
from ulid import ULID

from mcp_table_editor.editor._config import EditorConfig
from mcp_table_editor.editor._range import Range
from mcp_table_editor.editor._selector import Selector


class Editor:
    def __init__(
        self,
        table: pd.DataFrame | None = None,
        config: EditorConfig | None = None,
    ) -> None:
        self.id = ULID().hex
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

    def sort(
        self, by: str | Sequence[str] | None = None, ascending: bool = True
    ) -> None:
        """
        Sort the table by the given column(s).

        Parameters
        ----------
        by : str | list[str] | None
            The column(s) to sort by. If None, sort by all columns.
            Default to None
        ascending : bool, default True
            Whether to sort in ascending order. If False, sort in descending order.
        """
        if isinstance(by, str):
            by = [by]
        elif by is None:
            by = self.table.columns.tolist()
        self.table.sort_values(by=by, ascending=ascending, inplace=True)

    def sort_by_values(
        self, columns: str | list[str], values: Sequence[str] | Sequence[Sequence[str]]
    ) -> None:
        """
        Sort the table by the given column(s) and values.

        Parameters
        ----------
        column : str | list[str]
            The columns to sort by.
        values : list[str] | list[list[str]]
            The values to sort by.
        """
        if isinstance(columns, str):
            columns = [columns]
            if not isinstance(values, list) or not isinstance(values[0], str):
                raise ValueError(
                    f"Unexpected type on input values, Expected list[str] but actual value: {values}"
                )
            values = [values]

        key_columns = [f"${col}-key" for col in columns]
        for key_column, column, value_list in zip(key_columns, columns, values):
            self.table[key_column] = self.table[column].map(
                lambda x: value_list.index(x) if x in value_list else len(value_list)
            )
        self.table.sort_values(by=key_columns, inplace=True)
        self.table.drop(columns=key_columns, inplace=True)

    def get_table(self) -> pd.DataFrame:
        """
        Get the table as a pandas DataFrame.
        """
        return self.table.loc[self.index, self.columns]

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
