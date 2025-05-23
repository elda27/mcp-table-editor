from io import StringIO

import pandas as pd
import pytest

from mcp_table_editor.editor import InMemoryEditor, InsertRule, Range
from mcp_table_editor.editor._config import EditorConfig
from mcp_table_editor.handler._crud_handler import (
    CrudHandler,
    CrudInputSchema,
    CrudOutputSchema,
    Operation,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture for a sample DataFrame."""
    data = {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}
    return pd.DataFrame(data, index=[10, 11, 12])  # Use non-zero index for clarity


@pytest.fixture
def editor_config() -> EditorConfig:
    """Fixture for EditorConfig."""
    return EditorConfig(max_columns=100, max_rows=1000)


@pytest.fixture
def editor(sample_df: pd.DataFrame, editor_config: EditorConfig) -> InMemoryEditor:
    """Fixture for Editor."""
    return InMemoryEditor(table=sample_df.copy(), config=editor_config)


# --- Test GET Operations ---


def test_crud_handler_get_column(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test GET operation with column selection."""
    args = CrudInputSchema(
        method=Operation.GET,
        columns=["A", "C"],
        rows=None,
        value=None,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df[["A", "C"]]

    assert result.method == Operation.GET
    assert isinstance(result.content, str)
    # Read CSV response back into DataFrame for comparison
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    assert result.json_content == expected_df.to_dict(orient="records")


def test_crud_handler_get_row(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test GET operation with row selection."""
    args = CrudInputSchema(
        method=Operation.GET,
        rows=[10, 12],
        columns=None,
        value=None,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.loc[[10, 12]]

    assert result.method == Operation.GET
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    assert result.json_content == expected_df.to_dict(orient="records")


def test_crud_handler_get_cell(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test GET operation with cell selection."""
    args = CrudInputSchema(
        method=Operation.GET,
        rows=[10, 11],
        columns=["B", "C"],
        value=None,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.loc[[10, 11], ["B", "C"]]

    assert result.method == Operation.GET
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    assert result.json_content == expected_df.to_dict(orient="records")


# --- Test UPDATE Operations ---


def test_crud_handler_update_column(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test UPDATE operation with column selection."""
    update_value = 100
    args = CrudInputSchema(
        method=Operation.UPDATE,
        columns=["B"],
        value=update_value,
        rows=None,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.copy()
    expected_df["B"] = update_value

    assert result.method == Operation.UPDATE
    # Update returns the modified selection
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    # Check original editor data is NOT changed (due to immutable selector)
    assert result.json_content == expected_df.to_dict(orient="records")
    pd.testing.assert_frame_equal(editor.table, sample_df)


def test_crud_handler_update_cell(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test UPDATE operation with cell selection."""
    update_value = 0
    args = CrudInputSchema(
        method=Operation.UPDATE,
        rows=[10],
        columns=["A", "C"],
        value=update_value,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.copy()
    expected_df.loc[10, ["A", "C"]] = int(update_value)

    assert result.method == Operation.UPDATE
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    assert result.json_content == expected_df.to_dict(orient="records")
    pd.testing.assert_frame_equal(editor.table, sample_df)


# --- Test DELETE Operations ---


def test_crud_handler_delete_column(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test DELETE operation with column selection."""
    args = CrudInputSchema(
        method=Operation.DELETE,
        columns=["A", "C"],
        rows=None,
        value=None,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.copy()
    expected_df[["A", "C"]] = pd.NA

    assert result.method == Operation.DELETE
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    # Delete returns the selection that was set to NA
    pd.testing.assert_frame_equal(
        result_df_from_csv.astype(object).fillna(pd.NA),  # CSV reads NA as object
        expected_df,
    )
    # JSON might represent NA differently (e.g., None), adjust assertion if needed
    # assert result.json_content == expected_df[["A", "C"]].to_dict(orient="records")
    pd.testing.assert_frame_equal(editor.table, sample_df)


# --- Test DROP Operations ---


def test_crud_handler_drop_column(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test DROP operation with column selection."""
    args = CrudInputSchema(
        method=Operation.DROP,
        columns=["B"],
        rows=None,
        value=None,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.drop(columns=["B"])

    assert result.method == Operation.DROP
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    # Drop returns the dataframe *after* dropping
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    assert result.json_content == expected_df.to_dict(orient="records")
    pd.testing.assert_frame_equal(editor.table, sample_df)


def test_crud_handler_drop_row(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test DROP operation with row selection."""
    args = CrudInputSchema(
        method=Operation.DROP,
        rows=[11],
        columns=None,
        value=None,
        insert_rule=InsertRule.ABOVE,
        insert_offset=None,
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.drop(index=[11])

    assert result.method == Operation.DROP
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    assert result.json_content == expected_df.to_dict(orient="records")
    pd.testing.assert_frame_equal(editor.table, sample_df)


# --- Test INSERT Operations ---


def test_crud_handler_insert_column(editor: InMemoryEditor, sample_df: pd.DataFrame):
    """Test INSERT operation for a column."""
    insert_value = 10
    args = CrudInputSchema(
        method=Operation.INSERT,
        columns=["D"],  # New column name
        value=insert_value,
        insert_offset=1,  # Position to insert at
        rows=None,
        insert_rule=InsertRule.ABOVE,  # Explicitly add default
    )
    handler = CrudHandler(editor)
    result = handler.handle(args)

    expected_df = sample_df.copy()
    expected_df.insert(1, "D", int(insert_value))

    assert result.method == Operation.INSERT
    result_df_from_csv = pd.read_csv(StringIO(result.content), index_col=0)
    pd.testing.assert_frame_equal(result_df_from_csv, expected_df)
    assert result.json_content == expected_df.to_dict(orient="records")
    pd.testing.assert_frame_equal(editor.table, sample_df)
