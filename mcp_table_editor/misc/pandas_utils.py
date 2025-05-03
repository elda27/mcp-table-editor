import pandas as pd


def merge_index(df_index: pd.DataFrame, *indexes: pd.Index) -> pd.Index:
    """Merge multiple indexes into a single index.
    A index is order by input dataframe index.
    """
    merged_index = pd.Index([], dtype=df_index.dtype)
    for index in indexes:
        merged_index = merged_index.union(index, sort=False)
    _, orders = merged_index.reindex(df_index)
    if orders is None:
        return df_index
    return merged_index[list(filter(lambda x: x != -1, orders))]
