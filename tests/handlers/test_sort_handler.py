import pandas as pd
import pytest

from mcp_table_editor.editor import EditorConfig, InMemoryEditor
from mcp_table_editor.handler._sort_handler import SortHandler, SortInputSchema


@pytest.fixture
def sample_df():
    data = {"A": [3, 1, 2], "B": ["x", "y", "z"]}
    return pd.DataFrame(data)


@pytest.fixture
def editor_config():
    return EditorConfig(max_columns=10, max_rows=10)


@pytest.fixture
def editor(sample_df, editor_config):
    return InMemoryEditor(table=sample_df.copy(), config=editor_config)


def test_sort_handler_ascending(editor, sample_df):
    handler = SortHandler(editor)
    args = SortInputSchema(by=["A"], ascending=True)
    result = handler.handle(args)
    expected = sample_df.sort_values(by=["A"], ascending=True)
    pd.testing.assert_frame_equal(
        pd.DataFrame(result.json_content), expected.reset_index(drop=True)
    )


def test_sort_handler_descending(editor, sample_df):
    handler = SortHandler(editor)
    args = SortInputSchema(by=["A"], ascending=False)
    result = handler.handle(args)
    expected = sample_df.sort_values(by=["A"], ascending=False)
    pd.testing.assert_frame_equal(
        pd.DataFrame(result.json_content), expected.reset_index(drop=True)
    )


def test_sort_handler_multiple_columns(editor):
    df = pd.DataFrame({"A": [2, 1, 2], "B": ["b", "a", "a"]})
    editor.table = df.copy()
    handler = SortHandler(editor)
    args = SortInputSchema(by=["A", "B"], ascending=True)
    result = handler.handle(args)
    expected = df.sort_values(by=["A", "B"], ascending=True)
    pd.testing.assert_frame_equal(
        pd.DataFrame(result.json_content), expected.reset_index(drop=True)
    )
