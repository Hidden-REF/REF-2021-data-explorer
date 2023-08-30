import pandas as pd
import streamlit as st

import codebook as cb


source_url = "https://results2021.ref.ac.uk/"

page_title = "REF 2021 Data Explorer"
st.set_page_config(page_title=page_title,
                   layout="centered",
                   initial_sidebar_state="expanded",
                   )

st.title(page_title)

# page content
# ------------
st.markdown("## Data source")
st.markdown(f"The data used in this app is from the [REF 2021 website]({source_url})"
            " (accessed 2023/08/10) and has been processed with [https://github.com/softwaresaved/ref-2021-analysis](https://github.com/softwaresaved/ref-2021-analysis)")

st.markdown("## About the REF 2021 process")

st.markdown("Submissions consisted of")
st.markdown("- outputs (e.g. journal articles, books, datasets, etc.)")
st.markdown("- impact case studies")
st.markdown("- research groups information")
st.markdown("- research income information")
st.markdown("- research environment statements for each institution and unit")
st.markdown("- doctoral degrees awarded")

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
    st.write(cb.OPEN_ACCESS_NAMES)
