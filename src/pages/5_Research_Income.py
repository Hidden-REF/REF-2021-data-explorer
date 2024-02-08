""" Research Income page """
import streamlit as st

import read_write as rw
import visualisations as vis
import shared_content as sh

PAGE = "income"

(dset, logs) = sh.prepare_page(PAGE)

vis.display_record_counts_table(dset, logs)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER, sh.HISTOGRAMS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)
    with tabs[1]:
        vis.display_histograms(dset)
with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset, do_histograms=True)

sh.sidebar_settings()
