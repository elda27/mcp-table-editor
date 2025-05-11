from typing import Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from mcp_table_editor.editor._range import Range
from mcp_table_editor.editor._selector import Selector


class SqlSelector(Selector):
    """
    SQL Selector class for handling SQL queries on a DataFrame.
    """

    def __init__(self, engine: Engine, cell_range: Range) -> None:
        self.engine = engine
        self.range = cell_range

    def display_dataframe(self, columns: pd.Index, rows: pd.Index) -> pd.DataFrame:
        """
        Get the selected dataframe for display using SQL.
        columns: pd.Index - columns to select
        rows: pd.Index - row indices to select (assumed to be primary key values)
        """
        col_str = ", ".join([f'"{col}"' for col in columns])
        # Assume table name is in self.range.table_name and PK is 'id'
        table = getattr(self.range, "table_name", "data")
        if rows is not None and len(rows) > 0:
            # TODO: using between when rows is a pair of values
            row_str = ",".join([repr(r) for r in rows])
            sql = f"SELECT {col_str} FROM {table} WHERE id IN ({row_str})"
        else:
            sql = f"SELECT {col_str} FROM {table}"
        return pd.read_sql_query(sql, self.engine)

    def selected_dataframe(self) -> pd.DataFrame:
        """
        Get the selected dataframe based on the range using SQL.
        """
        # Assume self.range has table_name, columns, and rows attributes
        table = getattr(self.range, "table_name", "data")
        columns = getattr(self.range, "columns", None)
        rows = getattr(self.range, "rows", None)
        if columns is None:
            col_str = "*"
        else:
            col_str = ", ".join([f'"{col}"' for col in columns])
        if rows is not None and len(rows) > 0:
            row_str = ",".join([repr(r) for r in rows])
            sql = f"SELECT {col_str} FROM {table} WHERE id IN ({row_str})"
        else:
            sql = f"SELECT {col_str} FROM {table}"
        return pd.read_sql_query(sql, self.engine)

    def drop(self) -> pd.DataFrame:
        """
        Drop the selected range from the table using SQL (returns the table after drop).
        """
        table = getattr(self.range, "table_name", "data")
        columns = getattr(self.range, "columns", None)
        rows = getattr(self.range, "rows", None)
        with self.engine.begin() as conn:
            if columns:
                for col in columns:
                    conn.execute(text(f"ALTER TABLE {table} DROP COLUMN {col}"))
            if rows:
                row_str = ",".join([repr(r) for r in rows])
                conn.execute(text(f"DELETE FROM {table} WHERE id IN ({row_str})"))
        # Return the updated table
        return pd.read_sql_table(table, self.engine)

    def delete(self) -> pd.DataFrame:
        """
        Set the selected range to NULL using SQL (returns the table after update).
        """
        table = getattr(self.range, "table_name", "data")
        columns = getattr(self.range, "columns", None)
        rows = getattr(self.range, "rows", None)
        with self.engine.begin() as conn:
            if columns and rows:
                for col in columns:
                    row_str = ",".join([repr(r) for r in rows])
                    conn.execute(
                        text(f"UPDATE {table} SET {col}=NULL WHERE id IN ({row_str})")
                    )
            elif columns:
                for col in columns:
                    conn.execute(text(f"UPDATE {table} SET {col}=NULL"))
            elif rows:
                row_str = ",".join([repr(r) for r in rows])
                col_names = pd.read_sql_table(table, self.engine).columns
                for col in col_names:
                    conn.execute(
                        text(f"UPDATE {table} SET {col}=NULL WHERE id IN ({row_str})")
                    )
        return pd.read_sql_table(table, self.engine)

    def get(self) -> pd.DataFrame:
        """
        Get the selected range from the table using SQL.
        """
        return self.selected_dataframe()

    def update(self, value: Any) -> pd.DataFrame:
        """
        Update the selected range in the table with a new value using SQL.
        """
        table = getattr(self.range, "table_name", "data")
        columns = getattr(self.range, "columns", None)
        rows = getattr(self.range, "rows", None)
        with self.engine.begin() as conn:
            if columns and rows:
                for col in columns:
                    row_str = ",".join([repr(r) for r in rows])
                    conn.execute(
                        text(
                            f"UPDATE {table} SET {col}={repr(value)} WHERE id IN ({row_str})"
                        )
                    )
            elif columns:
                for col in columns:
                    conn.execute(text(f"UPDATE {table} SET {col}={repr(value)}"))
            elif rows:
                row_str = ",".join([repr(r) for r in rows])
                col_names = pd.read_sql_table(table, self.engine).columns
                for col in col_names:
                    conn.execute(
                        text(
                            f"UPDATE {table} SET {col}={repr(value)} WHERE id IN ({row_str})"
                        )
                    )
        return pd.read_sql_table(table, self.engine)

    def insert(
        self, pos: int | str | None = None, value: Any = pd.NA, insert_rule=None
    ) -> pd.DataFrame:
        """
        Insert a value (row/column) into the table using SQL.
        """
        table = getattr(self.range, "table_name", "data")
        columns = getattr(self.range, "columns", None)
        rows = getattr(self.range, "rows", None)
        with self.engine.begin() as conn:
            if columns and value is not pd.NA:
                # Add new columns
                for col in columns:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} TEXT"))
                    conn.execute(text(f"UPDATE {table} SET {col}={repr(value)}"))
            if rows and value is not pd.NA:
                # Add new rows
                col_names = pd.read_sql_table(table, self.engine).columns
                for r in rows:
                    values = ",".join([repr(value)] * len(col_names))
                    conn.execute(
                        text(
                            f"INSERT INTO {table} ({', '.join(col_names)}) VALUES ({values})"
                        )
                    )
        return pd.read_sql_table(table, self.engine)
