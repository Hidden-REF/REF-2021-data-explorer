# pylint: disable=C0103
""" Home page of the app. """
import streamlit as st
import shared_content as sh

PAGE = "home"

(_, _) = sh.prepare_page(PAGE)

st.markdown(sh.ABOUT_TEXT)

st.header(sh.DATA_SOURCE_HEADER)
st.markdown(sh.DATA_SOURCE_TEXT)
