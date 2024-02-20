# pylint: disable=E0401
# pylint: disable=W0718
"""Interact with the REF dataset using natural language queries to openai models.
"""
import textwrap
import logging
import json
from pathlib import Path
from typing import Optional, Literal, TypedDict, Union, Tuple
import pandas as pd
import pyarrow.dataset
import pyarrow.acero
import duckdb
import streamlit as st

from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_dtype,
    is_datetime64_ns_dtype,
)

import REF2021_explorer.read_write as rw
import REF2021_explorer.shared_content as sh

DEFAULT_MODEL = "gpt-3.5-turbo"

NULL_VALUES = ["NA", "N/A", "NK", "None"]


class SchemaField(TypedDict):
    """Field in a table schema"""

    name: str
    type: str
    distinct_values: list[str] | None


class TableInfo(TypedDict):
    """Table schema information"""

    rows: int
    columns: list[SchemaField]


def unique_values(dataset: pyarrow.dataset.Dataset, column: str) -> list[str]:
    """Returns unique values in a column of a dataset"""

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
    """Returns the type of a column in a parquet file"""

    if column.get("numpy_type") == "object" or column.get("pandas_type") == "unicode":
        return "string"

    return column.get("pandas_type") or column.get("numpy_type") or "string"


def get_schema(file: Path, enum_columns: None) -> TableInfo:
    """Returns parquet file schema as a dictionary of tables that can be passed to the LLM

    Args:
        db (str): Filename of file in parquet format
        enum_columns (list[str]): List of columns that should be considered
            enumerations, i.e the unique items in that column will be
            visible to the LLM; defaults to None

    Returns:
        Mapping of table names to list of SchemaField dictionaries
    """

    if enum_columns is None:
        enum_columns = []
    ds = pyarrow.dataset.dataset(file)
    metadata = ds.schema.metadata
    metadata_schema_bytes = metadata[list(metadata.keys())[0]]
    metadata_schema = json.loads(metadata_schema_bytes.decode("utf-8"))
    out_schema: TableInfo = {"rows": ds.count_rows(), "columns": []}
    for column in metadata_schema["columns"]:
        if column["name"] is None:  # skip unnamed columns, usually pandas indices
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
    """Returns the type of visualisation that should be used for the data

    Args:
        data (pd.DataFrame): Data to be visualised

    Returns:
        str: Type of visualisation to be used
    """

    # convert dates
    logging.debug("Data types: %s", data.dtypes)
    data.rename(columns={0: "Column"}, inplace=True)

    # one row or empty dataframe does not need visualisation
    if len(data) <= 1:
        return None
    # try to infer possible visualisation types based on datatypes
    # one column (series) data can usually be mapped as a histogram
    numeric_columns = [c for c in data.columns if is_numeric_dtype(data[c])]
    logging.debug("Numeric columns: %s", numeric_columns)
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

    if {"Country_ISO3", "Location"} & set(data.columns):
        return "map"

    return "bar"


def postprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Postprocesses the data to make it suitable for visualisation

    Args:
        df (pd.DataFrame): Data to be postprocessed

    Returns:
        pd.DataFrame: Postprocessed data
    """

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


def run_sql(sql_stmt: str) -> Union[str, pd.DataFrame]:
    """Runs a SQL statement and returns the results

    Args:
        sql_stmt (str): SQL statement to be executed

    Returns:
        Union[str, pd.DataFrame]: Results of the SQL statement
    """

    results = list(duckdb.query(sql_stmt.replace("`", '"')).fetchall())
    print("RESULTS", results)
    if len(results) == 1 and len(results[0]) == 1:
        return str(results[0][0])

    return postprocess_data(pd.DataFrame(results).replace(NULL_VALUES, None))


def get_sql(
    client, query: str, prompt: str, model: str = DEFAULT_MODEL
) -> Optional[str]:
    """Generates a SQL query from a natural language query using the OpenAI API

    Args:
        client: OpenAI API client
        query (str): Natural language query
        prompt (str): Prompt for the OpenAI model
        model (str, optional): OpenAI model to use. Defaults to DEFAULT_MODEL.

    Returns:
        Optional[str]: SQL query generated from the natural language query
    """

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

    return content


def clear_chat():
    """Clears the chat history"""

    st.session_state.messages = []


def show_data(
    df: pd.DataFrame,
    viz_type: Optional[Literal["bar", "line", "map"]] = None,
    drop_na: bool = True,
):
    """Displays the data in a dataframe and a visualisation of the data

    Args:
        df (pd.DataFrame): Data to be displayed
        viz_type (Optional[str], optional): Type of visualisation to use. Defaults to None.
        drop_na (bool, optional): Whether to drop NaN values. Defaults to True.
    """

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
    """Converts a table schema to a string

    Args:
        schema (TableInfo): Table schema

    Returns:
        str: String representation of the table schema
    """

    text = [f"CREATE TABLE '{rw.CHAT_DB}' ("]
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
    client, user_message: str, schema: str
) -> Tuple[Union[str, pd.DataFrame], Optional[str]]:
    """Asks the OpenAI model a question

    Args:
        client: OpenAI API client
        user_message (str): User message
        schema (str): Schema of the data

    Returns:
        Tuple[Union[str, pd.DataFrame], Optional[str]]:
            Response from the OpenAI model and the SQL query
    """

    prompt = sh.CHAT_PROMPT.format(schema=schema)
    try:
        query = get_sql(client, user_message.replace("%", ""), prompt)
    except NameError:  # client is not defined
        return sh.TOKEN_NOTAVAILABLE, None
    if query is None:
        return sh.NO_ANSWER, None
    if query.lower().strip().startswith("select"):
        try:
            print("> Using query:", query)
            results = run_sql(query)
            return results, query

        except Exception:
            return sh.NO_ANSWER, None
    else:
        return query, None


def sql_query_explanation(query: str) -> str:
    """Returns an explanation of the SQL query

    Args:
        query (str): SQL query

    Returns:
        str: Explanation of the SQL query
    """

    wrapped_query = "\n".join(textwrap.wrap(query))
    return f"""I used this query:
```sql
  {wrapped_query}
```"""
