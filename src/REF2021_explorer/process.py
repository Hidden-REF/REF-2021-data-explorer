# pylint: disable=E0401
""" Functions for processing the data. """
import numpy as np
import REF2021_explorer.codebook as cb


def calculate_counts(dset, col, sort=True):
    """Calculate counts and percentages for a column.

    Args:
        dset (pandas.DataFrame): The dataset to use.
        col (str): The column to use
        sort (bool): Whether to sort the counts.
    """

    col_count = "records"
    col_perc = "records (%)"
    dset_stats = (
        dset[col]
        .cat.remove_unused_categories()
        .value_counts(sort=sort)
        .to_frame(name=col_count)
    )
    dset_stats[col_perc] = np.round(100 * dset_stats[col_count] / dset.shape[0])
    dset_stats.index.name = col

    return dset_stats


def calculate_grouped_counts(dset, columns):
    """Calculate counts and percentages for a grouped dataset.

    Args:
        dset (pandas.DataFrame): The dataset to use.
        columns (list): The columns to use for grouping.

    Returns:
        dset_stats (pandas.DataFrame): The grouped dataset.
    """

    col_count = "records"
    col_perc = "records (%)"

    dset_stats = (
        dset[columns].groupby(columns, observed=True).size().to_frame(name=col_count)
    )
    dset_stats[col_perc] = np.round(
        100 * dset_stats[col_count] / dset_stats[col_count].sum()
    )

    return dset_stats.reset_index()


def get_column_lists(dset, dtype):
    """Get a list of columns of a given data type.

    Args:
        dset (pandas.DataFrame): The dataset to use.
        dtype (str): The data type to use.

    Returns:
        columns (list): The list of columns.
    """

    column_list = []
    if dtype == "category":
        column_list = [
            column
            for column in dset.columns
            if (dset[column].dtype.name == dtype)
            & (column not in cb.CATEGORY_FIELDS_EXCLUDE_CHARTS)
        ]
    elif dtype == "number":
        dtypes = ["int64", "float64"]
        column_list = [
            column for column in dset.columns if dset[column].dtype.name in dtypes
        ]

    return column_list
