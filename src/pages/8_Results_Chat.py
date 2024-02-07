""" Results chat page """
import os
import json
from pathlib import Path
import pandas as pd
import openai
import streamlit as st
import pyarrow.parquet as pq

import shared_text as sh
import read_write as rw
import chat


OPENAITOKEN_AVAILABLE = False

# get the categorical columns
pfile = pq.ParquetFile(rw.CHAT_DB)
json_struct = json.loads(pfile.metadata.metadata[b"pandas"])
ENUM_COLUMNS = [
    column["name"]
    for column in json_struct["columns"]
    if column["pandas_type"] == "categorical"
]

SCHEMA = chat.get_schema(Path(rw.CHAT_DB), ENUM_COLUMNS)
SCHEMA_TEXT = chat.schema_to_text(SCHEMA)

PAGE_TITLE = sh.CHAT_TITLE

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=sh.LAYOUT,
    initial_sidebar_state=sh.INITIAL_SIDEBAR_STATE,
    menu_items=sh.MENU_ITEMS,
)

st.title(PAGE_TITLE)


with st.sidebar:
    st.markdown(sh.CHAT_SIDEBAR_TEXT)
    api_key_input = st.text_input(
        sh.OPENAI_KEY_PROMPT,
        type="password",
        key="OPENAI_API_KEY",
        placeholder=sh.OPENAI_KEY_PLACEHOLDER,
        help=sh.OPENAI_KEY_HELP,  # noqa: E501
        value=os.environ.get("OPENAI_API_KEY", st.session_state.get("OPENAI_API_KEY")),
    )
    st.button(sh.CLEAR_CHAT_BUTTON, on_click=chat.clear_chat)

try:
    client = openai.OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
    OPENAITOKEN_AVAILABLE = True
except openai.OpenAIError:
    pass


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

    if not OPENAITOKEN_AVAILABLE:
        st.session_state.messages.append(
            {"role": "assistant", "content": sh.TOKEN_NOTAVAILABLE}
        )


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], pd.DataFrame):
            chat.show_data(message["content"], message.get("viz_type"))
        else:
            st.markdown(message["content"])
        if message.get("explanation"):
            st.markdown(chat.sql_query_explanation(message["explanation"]))

if query := st.chat_input("Enter your query here"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    ALTERNATE_RESPONSES = None
    VIZ_TYPE = None
    SQL_QUERY = None
    RESPONSE = None
    if ALTERNATE_RESPONSES:
        RESPONSE = ALTERNATE_RESPONSES
    else:
        try:
            RESPONSE, SQL_QUERY = chat.ask(client, query, SCHEMA_TEXT)
        except openai.AuthenticationError:  # type: ignore
            st.error(sh.OPENAI_KEY_ERROR, icon="🚨")
            st.stop()

    with st.chat_message("assistant"):
        if isinstance(RESPONSE, pd.DataFrame) and not RESPONSE.empty:
            print(RESPONSE.dtypes)
            VIZ_TYPE = chat.get_viz_type(RESPONSE)
            print(">> Inferred viz type:", VIZ_TYPE)
            chat.show_data(RESPONSE, VIZ_TYPE)
        elif isinstance(RESPONSE, pd.DataFrame) and RESPONSE.empty:
            RESPONSE = "I could not find any data for this question"
            st.markdown(RESPONSE)
        else:
            st.markdown(RESPONSE)
        if SQL_QUERY:
            st.markdown(chat.sql_query_explanation(SQL_QUERY))
    session_state = {
        "role": "assistant",
        "content": RESPONSE,
        "viz_type": VIZ_TYPE,
        "explanation": SQL_QUERY,
    }
    st.session_state.messages.append(session_state)
