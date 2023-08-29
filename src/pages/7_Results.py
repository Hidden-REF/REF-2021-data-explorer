import pandas as pd
import streamlit as st

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis


page_title = "Results"
st.title(page_title)

with st.spinner(rw.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_RESULTS)
    
dset_to_print = pd.DataFrame.from_dict(
    {
        "Results records": dset.shape[0],
        "Institutions": dset[cb.COL_INST_NAME].nunique()
    },
    orient="index"
    )
dset_to_print.columns = ["count"]
pd.set_option("display.max_colwidth", None)
st.dataframe(dset_to_print)

st.markdown("Select from the charts below to view the "
            "distributions for the number of results records by ...")
columns = [cb.COL_PANEL_NAME,
           cb.COL_UOA_NAME,
           cb.COL_RESULTS_PERC_STAFF_SUBMITTED_BINNED,
           cb.COL_RESULTS_4star_BINNED,
           cb.COL_RESULTS_3star_BINNED,
           cb.COL_RESULTS_2star_BINNED,
           cb.COL_RESULTS_1star_BINNED,
           cb.COL_RESULTS_UNCLASSIFIED_BINNED
           ]
tabs = st.tabs([column.replace(" stars", "*").replace(" star", "*").replace(" (binned)", "")
                for column in columns])
for i, column in enumerate(columns):
    with tabs[i]:
        dset_stats = proc.calculate_counts(dset,
                                           column,
                                           sort=False)
        vis.draw_counts_percent_chart(dset_stats,
                                      column)
