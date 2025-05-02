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
        # Ensure the selector works on a copy to maintain immutability
        self.df = df.copy()
        self.range = cell_range
        self.editor_config = editor_config

    def _update(self, df: pd.DataFrame) -> None:
        """
        Update the internal dataframe with a new one.
        This is used to maintain immutability in the editor.
        """
        self.df = df

    def selected_dataframe(self) -> pd.DataFrame:
        """
        Get the selected dataframe based on the range.
        """
        return self._get_range(self.range)

    def drop(self) -> pd.DataFrame:
        """Drop the selected range from the dataframe.

        Returns
        -------
        pd.DataFrame
            A new dataframe after dropping the selected range.
        """
        df = self.df.copy()  # Work on a copy
        if self.range.is_column_range():
            df = df.drop(columns=self.range.get_columns())  # Not inplace
        if self.range.is_index_range():
            df = df.drop(index=self.range.get_index())  # Not inplace
        if self.range.is_location_range():
            _, columns_to_drop = self.range.get_location()
            df = df.drop(columns=columns_to_drop)  # Not inplace
        self._update(df)
        return df  # Return the modified copy

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

    def delete(self) -> pd.DataFrame:
        """Delete (set to NA) the selected range from the dataframe.

        Returns
        -------
        pd.DataFrame
            A new dataframe with the selected range set to NA.
        """
        df = self.df.copy()  # Work on a copy
        if self.range.is_column_range():
            df[self.range.get_columns()] = pd.NA
        if self.range.is_index_range():
            df.loc[self.range.get_index()] = pd.NA
        if self.range.is_location_range():
            index, columns = self.range.get_location()
            df.loc[index, columns] = pd.NA
        self._update(df)
        return df  # Return the modified copy

    def get(self) -> pd.DataFrame:
        """Get the selected range from the dataframe.

        Returns
        -------
        pd.DataFrame
            The selected range from the dataframe.
        """
        return self._get_range(self.range)

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
        df = self.df.copy()  # Work on a copy
        if self.range.is_column_range():
            df[self.range.get_columns()] = value
        if self.range.is_index_range():
            df.loc[self.range.get_index()] = value
        if self.range.is_location_range():
            index, columns = self.range.get_location()
            df.loc[index, columns] = value
        self._update(df)
        return df  # Return the modified copy

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
        df = self.df.copy()  # Work on a copy

        if self.range.is_column_range():
            cols_to_insert = self.range.get_columns()
            insert_pos = pos if pos is not None else len(df.columns)
            if isinstance(insert_pos, str):
                raise TypeError(
                    "Position 'pos' must be an integer for column insertion."
                )

            current_pos = insert_pos
            for i, col in enumerate(cols_to_insert):
                df.insert(loc=current_pos + i, column=col, value=value)

        elif self.range.is_index_range():
            index_to_insert = self.range.get_index()
            new_rows_df = pd.DataFrame(value, index=index_to_insert, columns=df.columns)
            df = pd.concat([df, new_rows_df], axis=0)

        elif self.range.is_location_range():
            raise ValueError("Insert operation is not supported for location ranges.")
        else:
            raise TypeError("Invalid range type for insert operation.")

        if insert_rule == InsertRule.ABOVE:
            df = df.ffill(axis=0)

        self._update(df)

        return df  # Return the modified copy
