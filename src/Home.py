import streamlit as st
import shared as sh

st.set_page_config(page_title=sh.HOME_TITLE,
                   layout="centered",
                   initial_sidebar_state="expanded",
                   menu_items={'About': sh.DATA_SOURCE_TEXT}
                   )

st.title(sh.HOME_TITLE)

# page content
# ------------
st.header(sh.DATA_SOURCE_HEADER)
st.markdown(sh.DATA_SOURCE_TEXT)

st.header(sh.ABOUT_HEADER)
st.markdown(sh.ABOUT_TEXT)
