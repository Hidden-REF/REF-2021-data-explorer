import pandas as pd
import streamlit as st

# data paths
DATA_PATH = (
    "https://github.com/softwaresaved/ref-2021-analysis/raw/main/data/processed/sheets/"
)
DATA_EXT = ".parquet"
DATA_PPROCESS = "_preprocessed"

DATA_PPROC_RGROUPS = f"{DATA_PATH}ResearchGroups{DATA_PPROCESS}{DATA_EXT}"
DATA_PPROC_OUTPUTS = f"{DATA_PATH}Outputs{DATA_PPROCESS}{DATA_EXT}"
DATA_PPROC_IMPACTS = f"{DATA_PATH}ImpactCaseStudies{DATA_PPROCESS}{DATA_EXT}"
DATA_PPROC_DEGREES = (
    f"{DATA_PATH}ResearchDoctoralDegreesAwarded{DATA_PPROCESS}{DATA_EXT}"
)
DATA_PPROC_RINCOME = f"{DATA_PATH}ResearchIncome{DATA_PPROCESS}{DATA_EXT}"
DATA_PPROC_RINCOMEINKIND = f"{DATA_PATH}ResearchIncomeInKind{DATA_PPROCESS}{DATA_EXT}"
DATA_PPROC_RESULTS = f"{DATA_PATH}Results{DATA_PPROCESS}{DATA_EXT}"


@st.cache_data
def get_data(fname):
    """Read the data from a parquet file.

    Args:
        fname (str): Filename of the file to read.

    Returns:
    """

    dset = pd.read_parquet(fname, engine="pyarrow")

    return dset
