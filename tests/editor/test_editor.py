import pandas as pd
import pytest

# Assuming Range, EditorConfig, Selector are importable from these paths
# Adjust imports based on your actual project structure
from mcp_table_editor.editor._config import EditorConfig
from mcp_table_editor.editor._range import Range
from mcp_table_editor.editor._selector import InsertRule, Selector


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture for a sample DataFrame."""
    data = {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}
    return pd.DataFrame(data, index=["X", "Y", "Z"])


@pytest.fixture
def editor_config() -> EditorConfig:
    """Fixture for EditorConfig."""
    # Provide default values for required arguments
    return EditorConfig(max_columns=100, max_rows=1000)


# --- Tests for selected_dataframe / get ---


def test_selector_selected_dataframe_column_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test selecting columns."""
    original_df = sample_df.copy()
    cell_range = Range(column=["A", "C"])
    selector = Selector(original_df, cell_range, editor_config)
    selected_df = selector.selected_dataframe()
    pd.testing.assert_frame_equal(selected_df, original_df[["A", "C"]])
    # Ensure original df is unchanged
    pd.testing.assert_frame_equal(selector.df, original_df)


def test_selector_selected_dataframe_index_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test selecting rows (index)."""
    original_df = sample_df.copy()
    cell_range = Range(row=["X", "Z"])
    selector = Selector(original_df, cell_range, editor_config)
    selected_df = selector.selected_dataframe()
    pd.testing.assert_frame_equal(selected_df, original_df.loc[["X", "Z"]])
    # Ensure original df is unchanged
    pd.testing.assert_frame_equal(selector.df, original_df)


def test_selector_selected_dataframe_location_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test selecting specific cells."""
    original_df = sample_df.copy()
    full_expected_df = original_df.copy()
    cell_range = Range(cell=(["X", "Y"], ["B", "C"]))
    selector = Selector(original_df, cell_range, editor_config)
    selected_df = selector.selected_dataframe()
    expected_df = original_df.loc[["X", "Y"], ["B", "C"]]
    pd.testing.assert_frame_equal(selected_df, expected_df)
    # Ensure original df is unchanged
    pd.testing.assert_frame_equal(selector.df, original_df)


def test_selector_get(sample_df: pd.DataFrame, editor_config: EditorConfig):
    """Test the get method (should be same as selected_dataframe)."""
    original_df = sample_df.copy()
    cell_range = Range(column=["B"])
    selector = Selector(original_df, cell_range, editor_config)
    selected_df = selector.get()
    pd.testing.assert_frame_equal(selected_df, original_df[["B"]])
    # Ensure original df is unchanged
    pd.testing.assert_frame_equal(selector.df, original_df)


# --- Tests for drop ---


def test_selector_drop_column_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test dropping columns returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(column=["B"])
    selector = Selector(original_df, cell_range, editor_config)
    result_df = selector.drop()
    expected_df = original_df.drop(columns=["B"])
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_drop_index_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test dropping rows returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(row=["Y"])
    selector = Selector(original_df, cell_range, editor_config)
    result_df = selector.drop()
    expected_df = original_df.drop(index=["Y"])
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_drop_location_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test dropping columns based on location range returns a new DataFrame."""
    original_df = sample_df.copy()
    # Drop columns B and C because they are involved in the location range
    cell_range = Range(cell=(["X", "Y"], ["B", "C"]))
    selector = Selector(original_df, cell_range, editor_config)
    result_df = selector.drop()
    expected_df = original_df.drop(columns=["B", "C"])
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


# --- Tests for delete ---


def test_selector_delete_column_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test deleting (setting to NA) columns returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(column=["A", "C"])
    selector = Selector(original_df, cell_range, editor_config)
    result_df = selector.delete()
    expected_df = original_df.copy()
    expected_df[["A", "C"]] = pd.NA
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_delete_index_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test deleting (setting to NA) rows returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(row=["X", "Z"])
    selector = Selector(original_df, cell_range, editor_config)
    result_df = selector.delete()
    expected_df = original_df.copy()
    expected_df.loc[["X", "Z"]] = pd.NA
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_delete_location_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test deleting (setting to NA) specific cells returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(cell=(["X", "Y"], ["B", "C"]))
    selector = Selector(original_df, cell_range, editor_config)
    result_df = selector.delete()
    expected_df = original_df.copy()
    expected_df.loc[["X", "Y"], ["B", "C"]] = pd.NA
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


# --- Tests for update ---


def test_selector_update_column_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test updating columns returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(column=["B"])
    selector = Selector(original_df, cell_range, editor_config)
    update_value = 100
    result_df = selector.update(update_value)
    expected_df = original_df.copy()
    expected_df["B"] = update_value
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_update_index_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test updating rows returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(row=["Y"])
    selector = Selector(original_df, cell_range, editor_config)
    update_value = -1
    result_df = selector.update(update_value)
    expected_df = original_df.copy()
    expected_df.loc["Y"] = update_value
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_update_location_range(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test updating specific cells returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(cell=(["X"], ["A", "C"]))
    selector = Selector(original_df, cell_range, editor_config)
    update_value = 0
    result_df = selector.update(update_value)
    expected_df = original_df.copy()
    expected_df.loc["X", ["A", "C"]] = update_value
    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


# --- Tests for insert ---


def test_selector_insert_column(sample_df: pd.DataFrame, editor_config: EditorConfig):
    """Test inserting a new column returns a new DataFrame."""
    original_df = sample_df.copy()
    cell_range = Range(column=["D"])  # Define the new column name via Range
    selector = Selector(original_df, cell_range, editor_config)
    insert_value = 10
    result_df = selector.insert(pos=1, value=insert_value)

    expected_df = original_df.copy()
    expected_df.insert(1, "D", insert_value)

    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_insert_row(sample_df: pd.DataFrame, editor_config: EditorConfig):
    """Test inserting a new row returns a new DataFrame."""
    original_df = sample_df.copy()
    new_index_label = "W"
    cell_range = Range(row=[new_index_label])  # Define the new row index via Range
    selector = Selector(original_df, cell_range, editor_config)
    insert_value = {"A": 10, "B": 11, "C": 12}  # Provide full row data
    result_df = selector.insert(value=insert_value)

    expected_df = original_df.copy()
    new_row = pd.DataFrame(insert_value, index=[new_index_label])
    expected_df = pd.concat([expected_df, new_row], axis=0)

    # Check the returned DataFrame is correct
    pd.testing.assert_frame_equal(result_df, expected_df)
    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_insert_location_range_raises_error(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test inserting with a location range raises ValueError."""
    original_df = sample_df.copy()
    cell_range = Range(cell=(["X"], ["A"]))
    selector = Selector(original_df, cell_range, editor_config)
    with pytest.raises(ValueError, match="Insert operation is not supported"):
        selector.insert(value=99)

    # Check the original DataFrame inside selector is unchanged
    pd.testing.assert_frame_equal(selector.df, original_df)


def test_selector_insert_column_with_ffill(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test inserting a column with ffill rule."""
    df_with_na = sample_df.copy()
    df_with_na.loc["Y", "A"] = pd.NA  # Introduce NA for ffill test
    original_df = df_with_na.copy()

    cell_range = Range(column=["D"])
    selector = Selector(original_df, cell_range, editor_config)
    # Insert with default NA, then ffill
    result_df = selector.insert(pos=1, value=pd.NA, insert_rule=InsertRule.ABOVE)

    expected_df = original_df.copy()
    expected_df.insert(1, "D", pd.NA)
    expected_df = expected_df.ffill(axis=0)

    pd.testing.assert_frame_equal(result_df, expected_df)
    pd.testing.assert_frame_equal(selector.df, expected_df)


def test_selector_insert_row_with_ffill(
    sample_df: pd.DataFrame, editor_config: EditorConfig
):
    """Test inserting a row with ffill rule."""
    original_df = sample_df.copy()
    new_index_label = "W"
    cell_range = Range(row=[new_index_label])
    selector = Selector(original_df, cell_range, editor_config)
    # Insert row with NAs, then ffill
    insert_value = pd.NA
    result_df = selector.insert(value=insert_value, insert_rule=InsertRule.ABOVE)

    expected_df = original_df.copy()
    new_row = pd.DataFrame(
        insert_value, index=[new_index_label], columns=original_df.columns
    )
    expected_df = pd.concat([expected_df, new_row], axis=0)
    expected_df = expected_df.ffill(axis=0)

    pd.testing.assert_frame_equal(result_df, expected_df)
    pd.testing.assert_frame_equal(selector.df, expected_df)
