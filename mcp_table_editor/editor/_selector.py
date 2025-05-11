from enum import Enum
from typing import Any, Protocol

import pandas as pd

from mcp_table_editor.editor._config import EditorConfig
from mcp_table_editor.editor._range import Range


class InsertRule(str, Enum):
    """
    Enum for insert rules.
    """

    ABOVE = "above"  # Fill above the selected cell
    EMPTY = "empty"  # Fill empty cells in the selected range

    def __str__(self) -> str:
        return self.value


class Selector(Protocol):
    def display_dataframe(self, columns: pd.Index, rows: pd.Index) -> pd.DataFrame:
        """
        Get the selected dataframe for display.
        This is used to get the dataframe in a format suitable for display.
        """
        ...

    def selected_dataframe(self) -> pd.DataFrame:
        """
        Get the selected dataframe based on the range.
        """
        ...

    def drop(self) -> pd.DataFrame:
        """Drop the selected range from the dataframe.

        Returns
        -------
        pd.DataFrame
            A new dataframe after dropping the selected range.
        """
        ...

    def delete(self) -> pd.DataFrame:
        """Delete (set to NA) the selected range from the dataframe.

        Returns
        -------
        pd.DataFrame
            A new dataframe with the selected range set to NA.
        """
        ...

    def get(self) -> pd.DataFrame:
        """Get the selected range from the dataframe.

        Returns
        -------
        pd.DataFrame
            The selected range from the dataframe.
        """
        ...

    def update(self, value: Any) -> pd.DataFrame:
        """Update the selected range in the dataframe with a new value.

        Parameters
        ----------
        value : Any
            The value to update the selected range with.

        Returns
        -------
        pd.DataFrame
            A new dataframe with the selected range updated.
        """
        ...

    def insert(
        self,
        pos: int | str | None = None,
        value: Any = pd.NA,
        insert_rule: InsertRule = InsertRule.ABOVE,
    ) -> pd.DataFrame:
        """Insert a value (row/column) into the dataframe.

        Parameters
        ----------
        pos : int | str | None, optional
            Offset where the column will be inserted. Used only for column insertion.
            Defaults to inserting at the end.
        value : Any, optional
            Value to fill the new row/column with. Defaults to pd.NA.
        insert_rule : InsertRule, optional
            Rule for filling values (e.g., ABOVE for ffill). Default is ABOVE.

        Returns
        -------
        pd.DataFrame
            A new dataframe with the value inserted.

        Raises
        ------
        ValueError
            If trying to insert with a location range (ambiguous operation).
        TypeError
            If the range type is invalid for insertion.
        """
        ...
