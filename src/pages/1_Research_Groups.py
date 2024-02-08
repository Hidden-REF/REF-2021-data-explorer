""" Research Groups page """
import streamlit as st

import visualisations as vis
import shared_content as sh

PAGE = "groups"

(dset, logs) = sh.prepare_page(PAGE)

vis.display_record_counts_table(dset, logs, description=sh.GROUPS_DESCRIPTION)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)

with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset)
