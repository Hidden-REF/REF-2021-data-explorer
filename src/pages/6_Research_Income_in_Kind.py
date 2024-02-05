import streamlit as st

import read_write as rw
import visualisations as vis
import shared_text as sh

page = "income_in_kind"

st.set_page_config(
    page_title=sh.PAGE_TITLES[page],
    layout=sh.LAYOUT,
    initial_sidebar_state=sh.INITIAL_SIDEBAR_STATE,
    menu_items=sh.MENU_ITEMS,
)

st.title(sh.PAGE_TITLES[page])

(dset, logs) = rw.get_dataframes(page)

vis.display_record_counts_table(dset, logs)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER,
                    sh.GROUPED_DISTRIBUTIONS_TAB_HEADER,
                    sh.HISTOGRAMS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)
    with tabs[1]:
        vis.display_grouped_distribution(dset)
    with tabs[2]:
        vis.display_histograms(dset)
with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset, do_histograms=True)
