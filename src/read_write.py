""" Module to read and write data from and to files. """
import pandas as pd
import fastparquet as fp
import streamlit as st

import codebook as cb

FETCHING_DATA = "Fetching data..."

# data paths
DATA_PATH = (
    "https://github.com/softwaresaved/ref-2021-analysis/raw/main/data/processed/sheets/"
)
LOGS_PATH = "https://github.com/softwaresaved/ref-2021-analysis/raw/main/logs/"

LOCAL_DATA_PATH = "data/"

# local data for use with fastparquet
LOCAL_SOURCES = ["results"]

DATA_EXT = ".parquet"
LOGS_EXT = ".log"

PARQUET_ENGINE = "pyarrow"

sources = {
    "data": {
        "groups": "ResearchGroups",
        "outputs": "Outputs",
        "impacts": "ImpactCaseStudies",
        "degrees": "ResearchDoctoralDegreesAwarded",
        "income": "ResearchIncome",
        "income_in_kind": "ResearchIncomeInKind",
        "results": "Results",
    },
}
sources["logs"] = sources["data"].copy()

for source in sources["data"]:
    if source in LOCAL_SOURCES:
        sources["data"][
            source
        ] = f"{LOCAL_DATA_PATH}{sources['data'][source]}{DATA_EXT}"
    else:
        sources["data"][source] = f"{DATA_PATH}{sources['data'][source]}{DATA_EXT}"

    sources["logs"][source] = f"{LOGS_PATH}{sources['logs'][source]}{LOGS_EXT}"


CHAT_DB = "data/Results.parquet"


@st.cache_data
def get_data(page):
    """Read the data from a parquet file.

    Args:
        page (str): The page to get the data for.

    Returns:
        (pandas.DataFrame): The data read from the file.
    """

    fname = sources["data"][page]
    columns_to_read = None
    if page in LOCAL_SOURCES:
        # filter out the environment statement columns for local data
        pf = fp.ParquetFile(fname)
        columns_to_read = [
            column
            for column in pf.columns
            if column not in cb.COLUMNS_UNIT_ENVIRONMENT_STATEMENTS
        ]

    dset = pd.read_parquet(fname, columns=columns_to_read, engine=PARQUET_ENGINE)

    return dset


@st.cache_data
def get_logs(page):
    """Read the processing logs

    Args:
        page (str): The page to get the logs for.

    Returns:
        (pandas.DataFrame): The data read from the file.
    """

    fname = sources["logs"][page]
    logs = pd.read_csv(fname, sep="\t", header=None)
    logs = logs.to_csv(header=False, index=False).replace('"', "")

    return logs


def get_dataframes(page):
    """Get the data and logs for a page.

    Args:
        page (str): The page to get the data for.

    Returns:
        (pandas.DataFrame, pandas.DataFrame): The data and logs.
    """

    with st.spinner(FETCHING_DATA):
        dset = get_data(page)
        logs = get_logs(page)

    return dset, logs
