import pandas as pd
from pandas.testing import assert_index_equal

from mcp_table_editor.misc.pandas_utils import merge_index


def test_merge_index_empty():
    """Test merging empty indexes."""
    df = pd.DataFrame({"A": [1, 2, 3]}, index=[0, 1, 2])
    result = merge_index(df.index)
    expected = pd.Index([], df.index.dtype)
    assert_index_equal(result, expected)


def test_merge_index_single():
    """Test merging a single index."""
    df = pd.DataFrame({"A": [1, 2, 3]}, index=[0, 1, 2])
    idx1 = pd.Index([1, 0])
    result = merge_index(df.index, idx1)
    expected = pd.Index([0, 1])
    assert_index_equal(result, expected)


def test_merge_index_non_overlapping():
    """Test merging non-overlapping indexes."""
    df = pd.DataFrame({"A": [1, 2, 3, 4]}, index=[0, 1, 2, 3])
    idx1 = pd.Index([0, 2])
    idx2 = pd.Index([1, 3])
    result = merge_index(df.index, idx1, idx2)
    expected = pd.Index([0, 1, 2, 3])
    assert_index_equal(result, expected)


def test_merge_index_overlapping():
    """Test merging overlapping indexes."""
    df = pd.DataFrame({"A": [1, 2, 3, 4]}, index=[0, 1, 2, 3])
    idx1 = pd.Index([0, 1, 2])
    idx2 = pd.Index([1, 2, 3])
    result = merge_index(df.index, idx1, idx2)
    expected = pd.Index([0, 1, 2, 3])
    assert_index_equal(result, expected)


def test_merge_index_reordering():
    """Test merging indexes that need reordering based on DataFrame index."""
    df = pd.DataFrame({"A": [1, 2, 3, 4]}, index=[3, 1, 0, 2])
    idx1 = pd.Index([0, 1])
    idx2 = pd.Index([2, 3])
    result = merge_index(df.index, idx1, idx2)
    # Expected order should match df.index
    expected = pd.Index([3, 1, 0, 2])
    assert_index_equal(result, expected)


def test_merge_index_with_extra_values():
    """Test merging indexes with values not present in the DataFrame index."""
    df = pd.DataFrame({"A": [1, 2, 3]}, index=[0, 1, 2])
    idx1 = pd.Index([0, 1, 5])  # 5 is not in df.index
    idx2 = pd.Index([1, 2, 6])  # 6 is not in df.index
    result = merge_index(df.index, idx1, idx2)
    # Values 5 and 6 should be dropped by reindex().dropna()
    expected = pd.Index([0, 1, 2])
    assert_index_equal(result, expected)


def test_merge_index_string_index():
    """Test merging with string indexes."""
    df = pd.DataFrame({"A": [1, 2, 3]}, index=["c", "a", "b"])
    idx1 = pd.Index(["a", "c"])
    idx2 = pd.Index(["b", "a"])
    result = merge_index(df.index, idx1, idx2)
    expected = pd.Index(["c", "a", "b"])  # Order matches df.index
    assert_index_equal(result, expected)


def test_merge_index_mixed_types_in_df_index_fails():
    """Test merging when df index has mixed types (should work if comparable)."""
    # Note: Pandas generally discourages mixed-type indexes, but let's test behavior.
    # The function relies on sorting, which might fail or behave unexpectedly with truly mixed types.
    # However, if types are comparable (like int and float), it might work.
    df = pd.DataFrame({"A": [1, 2, 3]}, index=[1, 2.0, 0])
    idx1 = pd.Index([0, 1])
    idx2 = pd.Index([2.0])
    result = merge_index(df.index, idx1, idx2)
    # Expected order should match df.index after sorting the union
    # Union: [0, 1, 2.0] -> Sorted: [0, 1, 2.0] -> Reindexed: [1, 2.0, 0]
    expected = pd.Index([1, 2.0, 0], dtype="float64")  # Pandas promotes to float
    assert_index_equal(result, expected)
