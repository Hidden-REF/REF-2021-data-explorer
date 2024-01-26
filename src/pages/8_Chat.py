"""
REFChat module

Interact with the REF dataset using natural language queries
"""

import openai
import pandas as pd
import streamlit as st
import shared as sh

import sqlite_utils
from typing import Optional, Literal

DB = "ref2021.db"
TABLE = "ref2021"
DEFAULT_MODEL = "gpt-3.5-turbo"
PROMPT = """

You are a research assistant for the Research Excellence Framework 2021. Data
is stored in SQLite within the ''ref2021' table. You must respond to questions
with a valid SQL query. Do not return any natural language explanation, only
the SQL query.

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

def get_schema(db: Path, enum_columns: list[str] = []) -> dict[str, TableInfo]:
    """Returns SQL schema as a dictionary of tables that can be passed to the LLM

    Args:
        db (str): SQLite database path
        enum_columns (list[str]): List of columns that should be considered
            enumerations, i.e the unique items in that column will be
            visible to the LLM.

    Returns:
        Mapping of table names to list of SchemaField dictionaries
    """
    schema = {}
    conn = sqlite3.connect(db)
    tables = [
        x[0]
        for x in (
            conn.cursor()
            .execute(
                "SELECT name from sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
            .fetchall()
        )
    ]

    for table in tables:
        cur = conn.cursor()
        nrows = cur.execute(f"SELECT COUNT(*) from {table}").fetchall()[0][0]
        fields = cur.execute(f"PRAGMA table_info('{table}');").fetchall()
        fields = [
            cast(SchemaField, dict(name=x[1], type=x[2], distinct_vals=None))
            for x in fields
        ]
        for f in fields:
            if f in enum_columns:
                f["distinct_values"] = [
                        x[0]
                        for x in cur.execute(
                            f"SELECT DISTINCT [{f['name']}] from {table}"
                        ).fetchall()
                        if isinstance(x[0], str) and x[0].strip() not in NULL_VALUES
                    ]

        schema[table] = {"rows": nrows, "columns": fields}
    return schema


def get_viz_type(data: pd.DataFrame) -> Optional[Literal["bar", "line", "map"]]:
    # convert dates
    logging.debug(f"Data types: {data.dtypes}")

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

def _postprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    if len(df.columns) == 1:  # you probably want a histogram for a value series
        df = df.value_counts().reset_index()

        # if the counts are all 1, these were possibly from a SELECT DISTINCT query
        if list(df["count"].unique()) == [1]:
            del df["count"]
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



def evaluate_sql(db: sqlite_utils.db.Database, sql_stmt: str) -> Union[str, pd.DataFrame]:
    results = list(db.query(sql_stmt))
    if len(results) == 1 and len(results[0].keys()) == 1:
        return str(list(results[0].values())[0])
    else:
        return postprocess_data(pd.DataFrame(results).replace(NULL_VALUES, None))



def get_sql(query: str, prompt: str, model: str=DEFAULT_MODEL) -> str:
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ],
    )
    content = completion.choices[0].message["content"]
    if content.lower().startswith("select"):
        return content.replace("\n", " ")
    else:
        return content

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
    elif viz_type == "map":
        # is it a choropleth or a circle plot?
        if "Country_ISO3" in df.columns and "Location" not in df.columns:
            fig = px.choropleth(
                df,
                locations="Country_ISO3",
                color=yax,
            )
            ct.plotly_chart(fig)
        elif "Location" in df.columns:
            df = df.merge(LOCATIONS, how="inner", on="Location")
            print(df.dtypes)
            print("Size:", yax)
            ct.map(df, size=yax)
        elif {"latitude", "lat", "longitude", "long"} & set(df.columns):
            ct.map(df, size=yax)
        else:
            pass
    else:
        raise ValueError(f"Unknown viz_type {viz_type}")
    dt.dataframe(df)


def schema_to_text(schema: dict[str, TableInfo]) -> dict[str, str]:
    text = {t: [] for t in schema.keys()}
    for table in sorted(schema.keys()):
        text[table].append(f"CREATE TABLE {table} (")
        for field in schema[table]["columns"]:
            if not field["name"].strip():
                continue
            if field.get("distinct_values"):
                text[table].append(
                    f"  {field['name']} AS ENUM "
                    + repr(field.get("distinct_values"))
                    .replace("[", "(")
                    .replace("]", ")")
                    + ","
                )
            else:
                text[table].append(f"  {field['name']} {field['type']},")
        text[table].extend([")", ""])
    return {k: "\n".join(v) for k, v in text.items()}


def ask(
        message: str, schema: str
) -> Tuple[Union[str, pd.DataFrame], Optional[str]]:
    prompt = PROMPT.format(schema=schema)
    query = get_sql(prompt)
    if query.lower().strip().startswith("select"):
        try:
            if self.verbose:
                print("> Using query:", query)
            results = self.evaluate_sql(query)
            return results, query

        except sqlite3.OperationalError:
            return NO_ANSWER, None
    else:
        return query, None

# Streamlit code begins
st.title(sh.CHAT_TITLE)
