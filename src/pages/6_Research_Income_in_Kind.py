import pandas as pd
import streamlit as st

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis


page_title = "Research Income in Kind"
st.title(page_title)

with st.spinner(rw.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_RINCOMEINKIND)

dset_to_print = pd.DataFrame.from_dict(
    {
        "Research income in kind records": dset.shape[0],
        "Institutions": dset[cb.COL_INST_NAME].nunique()
    },
    orient="index"
    )
dset_to_print.columns = ["count"]
pd.set_option("display.max_colwidth", None)
st.dataframe(dset_to_print)

st.markdown("Select from the charts below to view the "
            "distributions for the number of research income in kind records by ...")


columns = [cb.COL_PANEL_NAME,
           cb.COL_UOA_NAME]
tabs = st.tabs(columns)

for i, column in enumerate(columns):
    with tabs[i]:
        dset_stats = proc.calculate_counts(dset,
                                           column,
                                           sort=False)
        vis.draw_counts_percent_chart(dset_stats,
                                      column)
