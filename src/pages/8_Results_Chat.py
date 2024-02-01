"""
REFChat module

Interact with the REF dataset using natural language queries
"""
import os
import openai
import pandas as pd
import streamlit as st
import pyarrow.parquet as pq
import json
from pathlib import Path

import shared_text as sh
import chat


OPENAITOKEN_AVAILABLE = False

# get the categorical columns
pfile = pq.ParquetFile(chat.DB)
json_struct = json.loads(pfile.metadata.metadata[b"pandas"])
ENUM_COLUMNS = [
    column["name"] for column in json_struct["columns"] if column["pandas_type"] == "categorical"
]

SCHEMA = chat.get_schema(Path(chat.DB), ENUM_COLUMNS)
SCHEMA_TEXT = chat.schema_to_text(SCHEMA)

# -----------------------------------------------------------------------
# Streamlit code begins
# -----------------------------------------------------------------------
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
        "Enter your OpenAI API Key to use the chat",
        type="password",
        key="OPENAI_API_KEY",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="You can get your API key from https://platform.openai.com/account/api-keys",  # noqa: E501
        value=os.environ.get("OPENAI_API_KEY", st.session_state.get("OPENAI_API_KEY")),
    )
    st.button("Clear chat", on_click=chat.clear_chat)

try:
    client = openai.OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
    OPENAITOKEN_AVAILABLE = True
except Exception:
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
    alternate_response = None
    viz_type = None
    sql_query = None
    response = None
    if alternate_response:
        response = alternate_response
    else:
        try:
            response, sql_query = chat.ask(client, query, SCHEMA_TEXT)
        except openai.AuthenticationError:  # type: ignore
            st.error("OpenAI authentication failed, try setting another key", icon="🚨")
            st.stop()

    with st.chat_message("assistant"):
        if isinstance(response, pd.DataFrame) and not response.empty:
            print(response.dtypes)
            viz_type = chat.get_viz_type(response)
            print(">> Inferred viz type:", viz_type)
            chat.show_data(response, viz_type)
        elif isinstance(response, pd.DataFrame) and response.empty:
            response = "I could not find any data for this question"
            st.markdown(response)
        else:
            st.markdown(response)
        if sql_query:
            st.markdown(chat.sql_query_explanation(sql_query))
    session_state = {
        "role": "assistant",
        "content": response,
        "viz_type": viz_type,
        "explanation": sql_query,
    }
    st.session_state.messages.append(session_state)
