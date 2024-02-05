import streamlit as st

import read_write as rw
import visualisations as vis
import shared_text as sh

PAGE_TITLE = sh.RESEARCH_GROUPS_TITLE

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=sh.LAYOUT,
    initial_sidebar_state=sh.INITIAL_SIDEBAR_STATE,
    menu_items=sh.MENU_ITEMS,
)

st.title(PAGE_TITLE)

with st.spinner(sh.PROC_TEXT):
    dset = rw.get_data(rw.DATA_GROUPS)
    logs = rw.get_logs(rw.LOGS_GROUPS)


vis.display_record_counts_table(dset, logs, description=sh.GROUPS_DESCRIPTION)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER, sh.GROUPED_DISTRIBUTIONS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)
    with tabs[1]:
        vis.display_grouped_distribution(dset)
with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset)
