import pandas as pd
import streamlit as st

# data paths
DATA_PATH = (
    "https://github.com/softwaresaved/ref-2021-analysis/raw/main/data/processed/sheets/"
)
LOGS_PATH = "https://github.com/softwaresaved/ref-2021-analysis/raw/main/logs/"

DATA_EXT = ".parquet"
LOGS_EXT = ".log"


DATA_GROUPS = f"{DATA_PATH}ResearchGroups{DATA_EXT}"
DATA_OUTPUTS = f"{DATA_PATH}Outputs{DATA_EXT}"
DATA_IMPACTS = f"{DATA_PATH}ImpactCaseStudies{DATA_EXT}"
DATA_DEGREES = (
    f"{DATA_PATH}ResearchDoctoralDegreesAwarded{DATA_EXT}"
)

DATA_INCOME = f"{DATA_PATH}ResearchIncome{DATA_EXT}"
DATA_INCOMEINKIND = f"{DATA_PATH}ResearchIncomeInKind{DATA_EXT}"
DATA_RESULTS = f"{DATA_PATH}Results{DATA_EXT}"

LOGS_GROUPS = f"{LOGS_PATH}ResearchGroups{LOGS_EXT}"
LOGS_OUTPUTS = f"{LOGS_PATH}Outputs{LOGS_EXT}"
LOGS_IMPACTS = f"{LOGS_PATH}ImpactCaseStudies{LOGS_EXT}"
LOGS_DEGREES = (
    f"{LOGS_PATH}ResearchDoctoralDegreesAwarded{LOGS_EXT}"
)
LOGS_INCOME = f"{LOGS_PATH}ResearchIncome{LOGS_EXT}"
LOGS_INCOMEINKIND = f"{LOGS_PATH}ResearchIncomeInKind{LOGS_EXT}"
LOGS_RESULTS = f"{LOGS_PATH}Results{LOGS_EXT}"

CHAT_DB = "db/Results_extra_preprocessed.parquet"


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
