import pandas as pd
import streamlit as st

# data paths
DATA_PATH = (
    "https://github.com/softwaresaved/ref-2021-analysis/raw/main/data/processed/sheets/"
)
LOGS_PATH = "https://github.com/softwaresaved/ref-2021-analysis/raw/main/logs/"

DATA_EXT = ".parquet"
LOGS_EXT = ".log"

PPROCESS_SUFFIX = "_preprocessed"


DATA_PPROC_RGROUPS = f"{DATA_PATH}ResearchGroups{PPROCESS_SUFFIX}{DATA_EXT}"
DATA_PPROC_OUTPUTS = f"{DATA_PATH}Outputs{PPROCESS_SUFFIX}{DATA_EXT}"
DATA_PPROC_IMPACTS = f"{DATA_PATH}ImpactCaseStudies{PPROCESS_SUFFIX}{DATA_EXT}"
DATA_PPROC_DEGREES = (
    f"{DATA_PATH}ResearchDoctoralDegreesAwarded{PPROCESS_SUFFIX}{DATA_EXT}"
)

DATA_PPROC_RINCOME = f"{DATA_PATH}ResearchIncome{PPROCESS_SUFFIX}{DATA_EXT}"
DATA_PPROC_RINCOMEINKIND = f"{DATA_PATH}ResearchIncomeInKind{PPROCESS_SUFFIX}{DATA_EXT}"
DATA_PPROC_RESULTS = f"{DATA_PATH}Results{PPROCESS_SUFFIX}{DATA_EXT}"

LOG_PPROC_RGROUPS = f"{LOGS_PATH}ResearchGroups{PPROCESS_SUFFIX}{LOGS_EXT}"
LOG_PPROC_OUTPUTS = f"{LOGS_PATH}Outputs{PPROCESS_SUFFIX}{LOGS_EXT}"
LOG_PPROC_IMPACTS = f"{LOGS_PATH}ImpactCaseStudies{PPROCESS_SUFFIX}{LOGS_EXT}"
LOG_PPROC_DEGREES = (
    f"{LOGS_PATH}ResearchDoctoralDegreesAwarded{PPROCESS_SUFFIX}{LOGS_EXT}"
)
LOG_PPROC_RINCOME = f"{LOGS_PATH}ResearchIncome{PPROCESS_SUFFIX}{LOGS_EXT}"
LOG_PPROC_RINCOMEINKIND = f"{LOGS_PATH}ResearchIncomeInKind{PPROCESS_SUFFIX}{LOGS_EXT}"
LOG_PPROC_RESULTS = f"{LOGS_PATH}Results{PPROCESS_SUFFIX}{LOGS_EXT}"


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
