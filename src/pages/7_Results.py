import streamlit as st

import codebook as cb
import read_write as rw
import visualisations as vis
import shared as sh

CATEGORIES_COLUMNS = [cb.COL_RESULTS_PROFILE]

page_title = "Results"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_RESULTS,
                            categories_columns=CATEGORIES_COLUMNS)

vis.display_record_counts_table(dset)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER,
                    sh.GROUPED_DISTRIBUTIONS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)
    with tabs[1]:
        vis.display_grouped_distribution(dset)
with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset)
