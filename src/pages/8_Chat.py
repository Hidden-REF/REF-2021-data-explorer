"""
REFChat module

Interact with the REF dataset using natural language queries
"""

import os
import json
import textwrap
import logging
from pathlib import Path
from typing import Optional, Literal, TypedDict, Union, Tuple

import openai

import duckdb
import pandas as pd
import pyarrow.dataset
import pyarrow.acero
import streamlit as st

from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_dtype,
    is_datetime64_ns_dtype,
)

import shared_text as sh

NO_ANSWER = "Sorry, I do not know the answer to that question."

TOKEN_NOTAVAILABLE = ":warning: Open AI token not available for the chat"

NULL_VALUES = ["NA", "N/A", "NK", "None"]

OPENAITOKEN_AVAILABLE = False

ENUM_COLUMNS = [
    "Institution name",
    "Main panel name",
    "Unit of assessment name",
    "Environment evaluation - 1 star (binned)",
    "Environment evaluation - 2 stars (binned)",
    "Environment evaluation - 3 stars (binned)",
    "Environment evaluation - 4 stars (binned)",
    "Environment evaluation - Unclassified (binned)",
    "Impact evaluation - 1 star (binned)",
    "Impact evaluation - 2 stars (binned)",
    "Impact evaluation - 3 stars (binned)",
    "Impact evaluation - 4 stars (binned)",
    "Impact evaluation - Unclassified (binned)",
    "Outputs evaluation - 1 star (binned)",
    "Outputs evaluation - 2 stars (binned)",
    "Outputs evaluation - 3 stars (binned)",
    "Outputs evaluation - 4 stars (binned)",
    "Outputs evaluation - Unclassified (binned)",
    "Overall evaluation - 1 star (binned)",
    "Overall evaluation - 2 stars (binned)",
    "Overall evaluation - 3 stars (binned)",
    "Overall evaluation - 4 stars (binned)",
    "Overall evaluation - Unclassified (binned)",
]

DB = "ref2021.parquet"
TABLE = "ref2021"
DEFAULT_MODEL = "gpt-3.5-turbo"
PROMPT = """

You are a research assistant for the Research Excellence Framework 2021. Data
is stored in parquet format within the 'ref2021.parquet' table. You must respond to questions
with a valid SQL query. Do not return any natural language explanation, only
the SQL query. Ensure that columns with spaces are quoted in the query.

If you are filtering using a WHERE clause, you must SELECT the columns being
filtered.

The dataset has the following schema:

{schema}
"""


class SchemaField(TypedDict):
    name: str
    type: str
    distinct_values: list[str] | None


class TableInfo(TypedDict):
    rows: int
    columns: list[SchemaField]


def unique_values(dataset: pyarrow.dataset.Dataset, column: str) -> list[str]:
    return (
        pyarrow.acero.Declaration.from_sequence(
            [
                pyarrow.acero.Declaration(
                    "scan", pyarrow.acero.ScanNodeOptions(dataset)
                ),
                pyarrow.acero.Declaration(
                    "aggregate", pyarrow.acero.AggregateNodeOptions([], [column])
                ),
            ]
        )
        .to_table()
        .column(0)
        .to_pylist()
    )


def get_column_type(column: dict[str, Optional[str]]) -> str:
    if column.get("numpy_type") == "object" or column.get("pandas_type") == "unicode":
        return "string"
    else:
        return column.get("pandas_type") or column.get("numpy_type") or "string"


def get_schema(file: Path, enum_columns: list[str] = []) -> TableInfo:
    """Returns parquet file schema as a dictionary of tables that can be passed to the LLM

    Args:
        db (str): Filename of file in parquet format
        enum_columns (list[str]): List of columns that should be considered
            enumerations, i.e the unique items in that column will be
            visible to the LLM.

    Returns:
        Mapping of table names to list of SchemaField dictionaries
    """
    ds = pyarrow.dataset.dataset(file)
    metadata = ds.schema.metadata
    metadata_schema_bytes = metadata[list(metadata.keys())[0]]
    metadata_schema = json.loads(metadata_schema_bytes.decode("utf-8"))
    out_schema: TableInfo = {"rows": ds.count_rows(), "columns": []}
    for column in metadata_schema["columns"]:
        if "Unnamed" in column["name"]:  # skip unnamed columns, usually pandas indices
            continue
        out_schema["columns"].append(
            {
                "name": column["name"],
                "type": get_column_type(column),
                "distinct_values": None,
            }
        )
        if column["name"] in enum_columns:
            out_schema["columns"][-1]["distinct_values"] = unique_values(
                ds, column["name"]
            )
    return out_schema


def get_viz_type(data: pd.DataFrame) -> Optional[Literal["bar", "line", "map"]]:
    # convert dates
    logging.debug(f"Data types: {data.dtypes}")
    data.rename(columns={0: "Column"}, inplace=True)

    # one row or empty dataframe does not need visualisation
    if len(data) <= 1:
        return None
    # try to infer possible visualisation types based on datatypes
    # one column (series) data can usually be mapped as a histogram
    numeric_columns = [c for c in data.columns if is_numeric_dtype(data[c])]
    logging.debug("Numeric columns: {numeric_columns}")
    if len(data.columns) > 1 and not is_numeric_dtype(data[data.columns[-1]]):
        return None
    if len(numeric_columns) > 2:  # multi-line not supported yet
        return None
    if any(
        "date_" in c.lower()
        or "_date" in c.lower()
        or c.endswith("Date")
        or c.endswith("Year")
        or is_datetime64_dtype(data[c])
        or is_datetime64_ns_dtype(data[c])
        for c in data.columns
    ):
        return "line"  # display time series as a line chart
    elif {"Country_ISO3", "Location"} & set(data.columns):
        return "map"
    else:
        return "bar"


def postprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    if len(df.columns) == 1:  # you probably want a histogram for a value series
        df = df.value_counts().reset_index(name="frequency")

        # if the counts are all 1, these were possibly from a SELECT DISTINCT query
        if list(df["frequency"].unique()) == [1]:
            del df["frequency"]
    df = df.apply(
        lambda col: pd.to_datetime(col, errors="ignore")
        if col.dtypes == object
        else col,
        axis=0,
    )
    if (
        len(
            date_columns := [
                c
                for c in df.columns
                if is_datetime64_dtype(df[c]) or is_datetime64_ns_dtype(df[c])
            ]
        )
        == 1
    ):
        df = df.sort_values(date_columns[0])
    return df


def run_sql(filename: str, sql_stmt: str) -> Union[str, pd.DataFrame]:
    results = list(duckdb.query(sql_stmt.replace("`", '"')).fetchall())
    if len(results) == 1 and len(results[0].keys()) == 1:
        return str(list(results[0].values())[0])
    else:
        return postprocess_data(pd.DataFrame(results).replace(NULL_VALUES, None))


def get_sql(query: str, prompt: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ],
    )
    content = completion.choices[0].message.content
    if content is None:
        return None
    if content.lower().startswith("select"):
        return content.replace("\n", " ")
    else:
        return content


def clear_chat():
    st.session_state.messages = []


def show_data(
    df: pd.DataFrame,
    viz_type: Optional[Literal["bar", "line", "map"]] = None,
    drop_na: bool = True,
):
    xax, yax = df.columns[0], df.columns[-1]
    if xax == yax or viz_type is None:
        st.dataframe(df)
        return
    ct, dt = st.tabs(["Chart", "Data"])
    if viz_type == "line":
        if drop_na:
            df = df[pd.notnull(df[xax])]
        ct.line_chart(df, x=xax, y=yax)
    elif viz_type == "bar":
        ct.bar_chart(df, x=xax, y=yax)
    elif viz_type == "map" and (
        {"latitude", "lat", "longitude", "long"} & set(df.columns)
    ):
        ct.map(df, size=yax)
    else:
        raise ValueError(f"Unknown viz_type {viz_type}")
    dt.dataframe(df)


def schema_to_text(schema: TableInfo) -> str:
    text = ["CREATE TABLE 'ref2021.parquet' ("]
    for field in schema["columns"]:
        if not field["name"].strip():
            continue
        if field.get("distinct_values"):
            text.append(
                f"  {field['name']} AS ENUM "
                + repr(field.get("distinct_values")).replace("[", "(").replace("]", ")")
                + ","
            )
        else:
            text.append(f"  {field['name']} {field['type']},")
    text.extend([")", ""])
    return "\n".join(text)


def ask(
    user_message: str, schema: str
) -> Tuple[Union[str, pd.DataFrame], Optional[str]]:
    prompt = PROMPT.format(schema=schema)
    try:
        query = get_sql(user_message.replace("%", ""), prompt)
    except NameError:  # client is not defined
        return TOKEN_NOTAVAILABLE, None
    if query is None:
        return NO_ANSWER, None
    if query.lower().strip().startswith("select"):
        try:
            print("> Using query:", query)
            results = run_sql(DB, query)
            return results, query

        except Exception:
            return NO_ANSWER, None
    else:
        return query, None


def sql_query_explanation(query: str) -> str:
    wrapped_query = "\n".join(textwrap.wrap(query))
    return f"""I used this query:
```sql
  {wrapped_query}
```"""


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

SCHEMA = get_schema(Path(DB), ENUM_COLUMNS)
SCHEMA_TEXT = schema_to_text(SCHEMA)

# pprint(SCHEMA)

with st.sidebar:
    st.markdown(sh.CHAT_SIDEBAR_TEXT)
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        key="OPENAI_API_KEY",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="You can get your API key from https://platform.openai.com/account/api-keys",  # noqa: E501
        value=os.environ.get("OPENAI_API_KEY", st.session_state.get("OPENAI_API_KEY")),
    )
    st.button("Clear chat", on_click=clear_chat)

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
            {"role": "assistant", "content": TOKEN_NOTAVAILABLE}
        )


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], pd.DataFrame):
            show_data(message["content"], message.get("viz_type"))
        else:
            st.markdown(message["content"])
        if message.get("explanation"):
            st.markdown(sql_query_explanation(message["explanation"]))

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
            response, sql_query = ask(query, SCHEMA_TEXT)
        except openai.AuthenticationError:  # type: ignore
            st.error("OpenAI authentication failed, try setting another key", icon="🚨")
            st.stop()

    with st.chat_message("assistant"):
        if isinstance(response, pd.DataFrame) and not response.empty:
            print(response.dtypes)
            viz_type = get_viz_type(response)
            print(">> Inferred viz type:", viz_type)
            show_data(response, viz_type)
        elif isinstance(response, pd.DataFrame) and response.empty:
            response = "I could not find any data for this question"
            st.markdown(response)
        else:
            st.markdown(response)
        if sql_query:
            st.markdown(sql_query_explanation(sql_query))
    session_state = {
        "role": "assistant",
        "content": response,
        "viz_type": viz_type,
        "explanation": sql_query,
    }
    st.session_state.messages.append(session_state)
