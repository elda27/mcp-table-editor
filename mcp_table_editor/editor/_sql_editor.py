import pandas as pd
import sqlalchemy as sa

from mcp_table_editor.editor._base import BaseEditor


class SqlEditor(BaseEditor):
    """
    SQL Editor class for handling SQL queries on a DataFrame.
    """

    def __init__(self, table: str = "sqlite:///:memory:") -> None:
        self.table = table
        self.engine = sa.create_engine(self.table)

    def query_sql(self, query: str) -> pd.DataFrame:
        """
        Query the table with a given SQL expression.

        Parameters
        ----------
        query : str
            The SQL expression to filter the table.

        Returns
        -------
        pd.DataFrame
            A DataFrame that contains the filtered table.
        """
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return pd.DataFrame(result.fetchall(), columns=result.keys()).set_index(
                "_id"
            )

    def query_expr(self, query: str) -> pd.DataFrame:
        """
        Query the table with a given query expression.

        Parameters
        ----------
        query : str
            The query expression to filter the table.

        Returns
        -------
        pd.DataFrame
            A DataFrame that contains the filtered table.
        """
        raise NotImplementedError(
            "Expression query is not implemented yet. Please use query_sql instead."
        )

    def select(self, range: str) -> SqlSelector:
