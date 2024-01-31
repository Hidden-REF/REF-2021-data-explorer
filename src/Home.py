import streamlit as st
import shared_text as sh

st.set_page_config(page_title=sh.HOME_TITLE,
                   page_icon="📊",
                   layout=sh.LAYOUT,
                   initial_sidebar_state="expanded",
                   menu_items={'Get Help': sh.REPO_URL,
                               'Report a bug': sh.REPO_URL,
                               'About': sh.DATA_SOURCE_TEXT
                               }
                   )


st.title(sh.HOME_TITLE)
st.warning(sh.WARNING_TEXT, icon="⚠️")


# page content
# ------------
st.header(sh.DATA_SOURCE_HEADER)
st.markdown(sh.DATA_SOURCE_TEXT)

st.header(sh.ABOUT_HEADER)
st.markdown(sh.ABOUT_TEXT)
