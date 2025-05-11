from typing import Protocol, Sequence

import pandas as pd

from mcp_table_editor.editor._range import Range
from mcp_table_editor.editor._selector import Selector


class BaseEditor(Protocol):
    """
    BaseEditor is a protocol that defines the interface for an editor.
    It is used to define the methods that an editor should implement.
    """

    def query_expr(self, query: str) -> pd.DataFrame:
        """
        Query the editor with a given expression.
        """
        ...

    def query_sql(self, query: str) -> pd.DataFrame:
        """
        Query the editor with a given SQL expression.
        """
        ...

    def select(self, range: Range) -> Selector:
        """
        Select a range in the editor.

        Parameters
        ----------
        range : Range
            The range to select in the editor.

        Returns
        -------
        Selector
            A Selector object that represents the selected range.
        """
        ...

    def query_expr(self, query: str) -> Selector:
        """
        Query the editor with a given expression.

        Parameters
        ----------
        query : str
            The expression to query the editor with.

        Returns
        -------
        Selector
            A Selector object that represents the result of the query.
        """
        ...

    def select(self, range: Range) -> Selector:
        """Select a range in the editor.

        Parameters
        ----------
        range : Range
            The range to select in the editor.

        Returns
        -------
        Selector
            A Selector object that represents the selected range.
        """
        ...

    def select_all(self) -> Selector:
        """
        Select all cells in the table.
        """
        ...

    def query(self, query: str) -> Selector:
        """
        Query the table with a given query string.

        Parameters
        ----------
        query : str
            The query string to filter the table.
        """
        ...

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
        ...

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
        ...

    def get_table(self) -> pd.DataFrame:
        """
        Get the table as a pandas DataFrame.
        """
        ...

    @property
    def columns(self) -> pd.Index:
        # Get the columns of the table.
        # TODO: If the table has too many columns, we should return a subset of the columns.
        # Note that it is controlled by the config.
        ...

    @property
    def index(self) -> pd.Index:
        # Get the rows of the table.
        # TODO: If the table has too many rows, we should return a subset of the rows.
        # Note that it is controlled by the config.
        ...
