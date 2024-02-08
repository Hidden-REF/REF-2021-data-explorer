""" Impact Case Studies page """
import streamlit as st

import read_write as rw
import visualisations as vis
import shared_content as sh

PAGE = "impacts"

st.set_page_config(
    page_title=sh.PAGE_TITLES[PAGE],
    layout=sh.LAYOUT,
    initial_sidebar_state=sh.INITIAL_SIDEBAR_STATE,
    menu_items=sh.MENU_ITEMS,
)

sh.sidebar_content(PAGE)

st.title(sh.PAGE_TITLES[PAGE])

(dset, logs) = rw.get_dataframes(PAGE)

vis.display_record_counts_table(dset, logs)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)

with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset)
