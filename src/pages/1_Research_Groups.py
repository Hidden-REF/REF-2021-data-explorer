""" Research Groups page """
import streamlit as st

import read_write as rw
import visualisations as vis
import shared_text as sh

PAGE = "groups"

st.set_page_config(
    page_title=sh.PAGE_TITLES[PAGE],
    layout=sh.LAYOUT,
    initial_sidebar_state=sh.INITIAL_SIDEBAR_STATE,
    menu_items=sh.MENU_ITEMS,
)

st.title(sh.PAGE_TITLES[PAGE])

(dset, logs) = rw.get_dataframes(PAGE)

vis.display_record_counts_table(dset, logs, description=sh.GROUPS_DESCRIPTION)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)

with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset)
