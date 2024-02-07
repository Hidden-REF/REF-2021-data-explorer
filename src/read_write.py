""" Module to read and write data from and to files. """
import pandas as pd
import streamlit as st

FETCHING_DATA = "Fetching data..."

# data paths
DATA_PATH = (
    "https://github.com/softwaresaved/ref-2021-analysis/raw/main/data/processed/sheets/"
)
LOGS_PATH = "https://github.com/softwaresaved/ref-2021-analysis/raw/main/logs/"

DATA_EXT = ".parquet"
LOGS_EXT = ".log"

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
    sources["data"][source] = f"{DATA_PATH}{sources['data'][source]}{DATA_EXT}"
    sources["logs"][source] = f"{LOGS_PATH}{sources['logs'][source]}{LOGS_EXT}"


CHAT_DB = "db/Results.parquet"


@st.cache_data
def get_data(fname):
    """Read the data from a parquet file.

    Args:
        fname (str): Filename of the file to read.

    Returns:
        (pandas.DataFrame): The data read from the file.
    """

    dset = pd.read_parquet(fname, engine="pyarrow")

    return dset


@st.cache_data
def get_logs(fname):
    """Read the processing logs

    Args:
        fname (str): Filename of the file to read.

    Returns:
        (pandas.DataFrame): The data read from the file.
    """

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
        dset = get_data(sources["data"][page])
        logs = get_logs(sources["logs"][page])

    return dset, logs
