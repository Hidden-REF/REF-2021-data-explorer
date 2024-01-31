import pandas as pd
import streamlit as st

import codebook as cb


# data paths
DATA_PATH = (
    "https://github.com/softwaresaved/ref-2021-analysis/raw/main/data/processed/sheets/"
)
DATA_EXT = ".csv.gz"
DATA_PPROCESS = "_ppreprocessed"

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
def get_data(fname, categories_columns=[], string_columns=[], drop_columns=[]):
    """Read a csv file and return a dataset and a list of institution names.

    Args:
        fname (str): Filename of the csv file to read.
        categories_columns (list): List of columns to be read as categories.
        string_columns (list): List of columns to be read as strings.
        drop_columns (list): List of columns to be dropped.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: Dataset read from the csv file.
            - list: List of institution names
    """

    # defines types to read
    dtype = {
        cb.COL_INST_CODE: "category",
        cb.COL_INST_NAME: "category",
        cb.COL_PANEL_NAME: "category",
        cb.COL_UOA_NAME: "category",
    }
    # binned percentages and various categories, depending on file
    binned_perc_columns = []
    if "Results_" in fname:
        binned_perc_columns = []
        for prefix in cb.COL_RESULTS_PROFILE_PREFIXES:
            binned_perc_columns.extend(
                [
                    f"{prefix} {cb.COL_RESULTS_1star_BINNED}",
                    f"{prefix} {cb.COL_RESULTS_2star_BINNED}",
                    f"{prefix} {cb.COL_RESULTS_3star_BINNED}",
                    f"{prefix} {cb.COL_RESULTS_4star_BINNED}",
                    f"{prefix} {cb.COL_RESULTS_UNCLASSIFIED_BINNED}",
                ]
            )

    for column in binned_perc_columns:
        dtype[column] = "category"

    for column in categories_columns:
        dtype[column] = "category"

    for column in string_columns:
        dtype[column] = "string"

    dset = pd.read_csv(fname, index_col=0, dtype=dtype)

    print(f"Read {fname}: {dset.shape[0]} records")

    # drop columns
    # dset.drop(columns=drop_columns, inplace=True)

    # set the category order for the binned percentages
    # for column in binned_perc_columns:
    #     dset[column] = pd.Categorical(dset[column],
    #                                   categories=cb.bin_percentages_labels())

    # get institution names as list
    inst_names = dset[cb.COL_INST_NAME].unique()

    return (dset, inst_names)


def download_data(dset, prompt, fname):
    """Download a dataset as a csv file.

    Args:
        dset (pandas.DataFrame): The dataset to download.
        prompt (str): The prompt to display for the download link.
    """
    st.download_button(
        label=prompt,
        data=dset.to_csv().encode("utf-8"),
        file_name=fname,
        mime="text/csv",
    )
