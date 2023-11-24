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

st.header("About the REF 2021 Explorer")
text_to_display = """

This site is currently under construction. Changes will be made on a frequent basis from November 2023 to
early in 2024. Until we announce that the website is complete, please do not use any of the results from
analysis you conduct on this site unless you have independently verified the results.

The Research Excellent Framework (REF) is the UK's approach to assessing the excellence of UK research. It is 
employs a process of expert review across all UK universities for 34 subject-based units of assessment. The
REF is conducted around every seven years, with the most recent taking place in 2021.

All of the data on this website is published openly on the REF 2021 website. This site is dedicated to
understanding the results of the REF 2021 by providing users with the ability to analyse and search the REF
data.

Submissions for REF 2021 consisted of data sets on
- Research Groups
- Outputs (e.g. journal articles, books, datasets, etc.)
- Impact Case Studies
- Doctoral Degrees Awarded
- Research Income
- Research Income in Kind
- Research Environment 

The website currently allows for any of the above information to be analysed and visualised. Select a data
set from the side bar, then use the main section of the website to choose elements of the data set to visualise.
You can also compare elements of the data set and visualise the results.


"""
st.markdown(text_to_display)
