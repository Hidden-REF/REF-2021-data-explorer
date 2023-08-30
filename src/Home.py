import pandas as pd
import streamlit as st

import codebook as cb
import shared as sh

page_title = "REF 2021 Data Explorer"
st.set_page_config(page_title=page_title,
                   layout="centered",
                   initial_sidebar_state="expanded",
                   menu_items={'About': sh.DATA_INFO}
                   )

st.title(page_title)

# page content
# ------------
st.header("Data source")
st.markdown(sh.DATA_INFO)

st.header("About the REF 2021 process")
text_to_display = """Submissions for REF 2021 consisted of
- Outputs (e.g. journal articles, books, datasets, etc.)
- Impact Case Studies
- Research Groups
- Research Income and Research Income in Kind
- Research Environment statements for each institution and unit
- Doctoral Degrees Awarded
"""
st.markdown(text_to_display)


columns = [cb.COL_PANEL_NAME,
           cb.COL_UOA_NAME,
           cb.COL_OUTPUT_TYPE_NAME,
           cb.COL_OPEN_ACCESS
           ]

tabs = st.tabs(columns)

# MAIN PANELS
# ------------
with tabs[0]:
    dset_to_print = pd.DataFrame.from_dict(cb.PANEL_NAMES,
                                           orient="index",
                                           columns=["Main Panel"])
    dset_to_print.index.name = "Code"
    st.dataframe(dset_to_print)

# UOAs
# ----
with tabs[1]:
    dset_to_print = pd.DataFrame.from_dict(cb.UOA_NAMES,
                                           orient="index",
                                           columns=["UOA"])
    dset_to_print.index.name = "Code"
    st.dataframe(dset_to_print)

# OUTPUT TYPES
# ------------
with tabs[2]:
    dset_to_print = pd.DataFrame.from_dict(cb.OUTPUT_TYPE_NAMES,
                                           orient="index",
                                           columns=["Output type"])
    dset_to_print.index.name = "Code"
    st.dataframe(dset_to_print)

# OPEN ACCESS
# -----------
with tabs[3]:
    dset_to_print = pd.DataFrame.from_dict(cb.OPEN_ACCESS_NAMES,
                                           orient="index",
                                           columns=["Output type"])
    dset_to_print.index.name = "Code"
    st.dataframe(dset_to_print)
