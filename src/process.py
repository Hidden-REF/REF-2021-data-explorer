""" Functions for processing the data. """


def calculate_counts(dset, col, sort=True):
    """ Calculate counts and percentages for a column.

    Args:
        dset (pandas.DataFrame): The dataset to use.
        col (str): The column to use
        sort (bool): Whether to sort the counts.
    """

    col_count = "records"
    col_perc = "records (%)"
    dset_stats = dset[col].value_counts(sort=sort).to_frame(name=col_count)
    dset_stats[col_perc] = 100 * dset_stats[col_count] / dset.shape[0]
    dset_stats.index.name = col

    return dset_stats


def calculate_grouped_counts(dset, columns):
    """ Calculate counts and percentages for a grouped dataset.

    Args:
        dset (pandas.DataFrame): The dataset to use.
        columns (list): The columns to use for grouping.

    Returns:
        dset_stats (pandas.DataFrame): The grouped dataset.
    """

    col_counts = "records"
    dset_stats = dset.groupby(columns).size().reset_index(name=col_counts)

    return dset_stats
