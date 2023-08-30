import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.chart_container import chart_container

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis
import shared as sh


CATEGORIES_COLUMNS = [cb.COL_INCOME_SOURCE]

page_title = "Research Income in Kind"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_RINCOMEINKIND,
                            categories_columns=CATEGORIES_COLUMNS)

vis.display_record_counts_table(dset)

# distribution charts
# -------------------
st.subheader(sh.CHARTS_HEADER)
dcolumns = [cb.COL_PANEL_NAME,
            cb.COL_UOA_NAME,
            cb.COL_INCOME_SOURCE]
dtabs = st.tabs(dcolumns)

for i, column in enumerate(dcolumns):
    with dtabs[i]:
        dset_stats = proc.calculate_counts(dset,
                                           column,
                                           sort=False)
        with chart_container(dset_stats):
            vis.draw_counts_percent_chart(dset_stats,
                                          column)

st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
st.dataframe(dset_explore, use_container_width=False)

# explore data
# ------------
st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
if (dset_explore.shape[0] < dset.shape[0]) & (dset_explore.shape[0] > 0):
    dict = {"Selected records": dset_explore.shape[0]}
    vis.display_table_from_dictionary(dict)
    rw.download_data(dset_explore,
                     sh.DOWNLOAD_SELECTED_DATA_PROMPT,
                     "selected_data.csv")
    st.dataframe(dset_explore, use_container_width=False)
