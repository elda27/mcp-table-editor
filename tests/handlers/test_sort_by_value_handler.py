import pandas as pd
import pytest

from mcp_table_editor.editor._config import EditorConfig
from mcp_table_editor.editor._in_memory_editor import InMemoryEditor
from mcp_table_editor.handler._sort_by_value_handler import (
    SortByValueHandler,
    SortByValueInputSchema,
)


@pytest.fixture
def sample_df():
    data = {"A": ["foo", "bar", "baz", "qux"], "B": [1, 2, 3, 4]}
    return pd.DataFrame(data)


@pytest.fixture
def editor(sample_df):
    return InMemoryEditor(table=sample_df.copy(), config=EditorConfig.default())


def test_sort_by_value_handler_single_column(editor, sample_df):
    handler = SortByValueHandler(editor)
    # Sorting order by: baz, foo, bar, qux
    values = [["baz", "foo", "bar", "qux"]]
    args = SortByValueInputSchema(by=["A"], values=values)
    result = handler.handle(args)
    # Making expected DataFrame after sorting
    expected = sample_df.set_index("A").loc[["baz", "foo", "bar", "qux"]].reset_index()
    pd.testing.assert_frame_equal(
        pd.DataFrame(result.json_content), expected.reset_index(drop=True)
    )


def test_sort_by_value_handler_multiple_columns(editor):
    df = pd.DataFrame(
        {"A": ["foo", "bar", "baz", "foo", "bar", "baz"], "B": [1, 2, 3, 4, 1, 2]}
    )
    editor.table = df.copy()
    handler = SortByValueHandler(editor)
    # Sorting order by multiple columns: A: baz, foo, bar; B: 4, 1, 2, 3
    values = [["baz", "foo", "bar"], [4, 1, 2, 3]]
    args = SortByValueInputSchema(by=["A", "B"], values=values)
    result = handler.handle(args)
    # Making expected DataFrame after sorting
    expected = df.copy()
    expected["A"] = ["baz", "baz", "foo", "foo", "bar", "bar"]
    expected["B"] = [2, 3, 4, 1, 1, 2]
    pd.testing.assert_frame_equal(
        pd.DataFrame(result.json_content), expected.reset_index(drop=True)
    )
