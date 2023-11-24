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
text_to_display = """Submissions for REF 2021 consisted of information on
- Research Groups
- Outputs (e.g. journal articles, books, datasets, etc.)
- Impact Case Studies
- Doctoral Degrees Awarded
- Research Income
- Research Income in Kind
- Research Environment 

Use the sidebar to navigate between the data sets to visualise and explore the data.
"""
st.markdown(text_to_display)
