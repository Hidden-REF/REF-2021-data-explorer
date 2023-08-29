import pandas as pd
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis
import shared as sh


page_title = "Impact Case Studies"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_IMPACTS)

dset_to_print = pd.DataFrame.from_dict(
    {
        "Impact case studies records": dset.shape[0],
        "Institutions": dset[cb.COL_INST_NAME].nunique()
    },
    orient="index"
    )
dset_to_print.columns = ["count"]
pd.set_option("display.max_colwidth", None)
st.dataframe(dset_to_print)

st.subheader(sh.CHARTS_HEADER)
st.markdown("Select from the charts below to view the "
            "distributions for the number of impact case studies records by ...")

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

st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
st.dataframe(dset_explore, use_container_width=False)
