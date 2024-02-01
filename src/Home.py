import streamlit as st
import shared_text as sh

PAGE_TITLE = sh.HOME_TITLE

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=sh.LAYOUT,
    initial_sidebar_state=sh.INITIAL_SIDEBAR_STATE,
    menu_items=sh.MENU_ITEMS,
)


st.title(PAGE_TITLE)
st.warning(sh.WARNING_TEXT, icon="⚠️")


# page content
# ------------
st.markdown(sh.ABOUT_TEXT)

st.header(sh.DATA_SOURCE_HEADER)
st.markdown(sh.DATA_SOURCE_TEXT)
