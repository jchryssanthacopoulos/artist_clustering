"""Utility functions."""

from scipy.sparse import coo_matrix


def cast_to_sparse_matrix(
        df, row_var='artistnum', col_var='usernum', var='total_streams',
        num_rows=None, num_cols=None):
    """Cast DataFrame to sparse matrix."""
    rows, cols = df[row_var], df[col_var]

    # infer dimensions from data
    if num_rows is None:
        num_rows = df[row_var].max() + 1
    if num_cols is None:
        num_cols = df[col_var].max() + 1

    return coo_matrix(
        (df[var], (rows, cols)),
        shape=(num_rows, num_cols))
