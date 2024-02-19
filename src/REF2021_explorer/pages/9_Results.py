# pylint: disable=C0103
# pylint: disable=R0801
# pylint: disable=E0401
""" Results page"""
import streamlit as st

import REF2021_explorer.visualisations as vis
import REF2021_explorer.shared_content as sh

PAGE = "results"

(dset, logs) = sh.prepare_page(PAGE)

vis.display_metrics(dset)

vis.display_data_explorer(dset)

with st.expander(sh.DESCRIBE_HEADER):
    vis.display_data_description(dset, description=sh.GROUPS_DESCRIPTION)

with st.expander(sh.LOGS_HEADER):
    vis.display_logs(logs)

# vis.display_record_counts_table(dset, logs, description=sh.RESULTS_DESCRIPTION)
# with st.expander(sh.VISUALISE_HEADER):
#     tabs = st.tabs(
#         [
#             sh.DISTRIBUTIONS_TAB_HEADER,
#             sh.HISTOGRAMS_TAB_HEADER,
#         ]
#     )
#     with tabs[0]:
#         vis.display_distributions(dset)
#     with tabs[1]:
#         vis.display_histograms(dset)
# with st.expander(sh.EXPLORE_HEADER):
#     vis.display_data_explorer(dset, do_histograms=True)
