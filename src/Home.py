""" Home page of the app. """
import streamlit as st
from streamlit_extras.app_logo import add_logo
import shared_content as sh
import visualisations as vis

PAGE = "home"

st.set_page_config(
    page_title=sh.PAGE_TITLES[PAGE],
    layout=sh.LAYOUT,
    initial_sidebar_state=sh.INITIAL_SIDEBAR_STATE,
    menu_items=sh.MENU_ITEMS,
)

sh.sidebar_content(PAGE)

st.title(sh.PAGE_TITLES[PAGE])
st.warning(sh.WARNING_TEXT, icon="⚠️")


# page content
# ------------
st.markdown(sh.ABOUT_TEXT)

st.header(sh.DATA_SOURCE_HEADER)
st.markdown(sh.DATA_SOURCE_TEXT)
