import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.chart_container import chart_container

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis
import shared as sh

CATEGORIES_COLUMNS = [cb.COL_RESULTS_PROFILE]

page_title = "Results"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_RESULTS,
                            categories_columns=CATEGORIES_COLUMNS)

vis.display_record_counts_table(dset)

# distribution charts
# -------------------
st.subheader(sh.CHARTS_HEADER)
dcolumns = [cb.COL_PANEL_NAME,
            cb.COL_UOA_NAME,
            cb.COL_RESULTS_PROFILE,
            cb.COL_RESULTS_PERC_STAFF_SUBMITTED_BINNED,
            cb.COL_RESULTS_4star_BINNED,
            cb.COL_RESULTS_3star_BINNED,
            cb.COL_RESULTS_2star_BINNED,
            cb.COL_RESULTS_1star_BINNED,
            cb.COL_RESULTS_UNCLASSIFIED_BINNED]
dtabs = st.tabs([column.replace(" stars", "*").replace(" star", "*").replace(" (binned)", "")
                for column in dcolumns])

for i, column in enumerate(dcolumns):
    with dtabs[i]:
        dset_stats = proc.calculate_counts(dset,
                                           column,
                                           sort=False)
        with chart_container(dset_stats):
            vis.draw_counts_percent_chart(dset_stats,
                                          column)

# explore data
# ------------
st.divider()
st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
st.dataframe(dset_explore, use_container_width=False)
