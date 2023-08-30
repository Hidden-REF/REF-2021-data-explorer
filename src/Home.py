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
           cb.COL_OPEN_ACCESS,
           cb.COL_INCOME_SOURCE,
           cb.COL_INCOMEINKIND_SOURCE
           ]

tabs = st.tabs(columns)

for itab, tab in enumerate(tabs):
    with tab:
        column = columns[itab]
        dict = cb.enum_values[column]
        dset_to_print = pd.DataFrame.from_dict(dict,
                                               orient="index",
                                               columns=[column])
        dset_to_print.index.name = "Code"
        st.dataframe(dset_to_print)
