# pylint: disable=C0103
# pylint: disable=R0801
""" Impact Case Studies page """
import streamlit as st

import REF2021_explorer.visualisations as vis
import REF2021_explorer.shared_content as sh

PAGE = "impacts"

(dset, logs) = sh.prepare_page(PAGE)

vis.display_metrics(dset)

vis.display_data_explorer(dset)

with st.expander(sh.DESCRIBE_HEADER):
    vis.display_data_description(dset, description=sh.GROUPS_DESCRIPTION)

with st.expander(sh.LOGS_HEADER):
    vis.display_logs(logs)
