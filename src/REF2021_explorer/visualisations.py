# pylint: disable=E0401
""" Visualisation functions. """
import importlib
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.chart_container import chart_container
from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit_scrollable_textbox as stx
import altair as alt

import REF2021_explorer.codebook as cb
import REF2021_explorer.process as proc
import REF2021_explorer.shared_content as sh

importlib.reload(sh)

USE_CONTAINER_WIDTH = True

TO_REPLACE_TITLES = {" stars": "* rating", " star": "* rating", " (binned)": ""}

STATS_TYPES = ["Counts", "Percentages"]

COLUMN_STATS = ["records", "records (%)"]

DESCRIPTION_MEASURES = ["min", "max", "mean", "std"]

BIN_OPTIONS = [5, 10, 25, 50]


def clean_titles(title):
    """Clean titles.

    Args:
        title (str): title

    Returns:
        str: cleaned title
    """

    for key, item in TO_REPLACE_TITLES.items():
        title = title.replace(key, item)

    return title


def show_counts_percent_chart(
    dset,
    title,
    column_name,
    columns_stats=None,
    stats_type="Percentages",
):
    """Draw a chart with counts and percentages.

    Args:
        dset (pandas.DataFrame): dataset
        column_stats (list): column names for the stats
        column_percent (str): column name for the percentages
        use_container_width (bool): use container width
    """

    if columns_stats is None:
        columns_stats = COLUMN_STATS

    stats_type_index = STATS_TYPES.index(stats_type)
    if stats_type_index == 0:
        domain = [0, dset[columns_stats[0]].max()]
    else:
        domain = [0, 100]

    with st.container(border=True):
        st.altair_chart(
            alt.Chart(dset.reset_index())
            .mark_bar()
            .encode(
                x=alt.X(
                    columns_stats[stats_type_index],
                    type="quantitative",
                    axis=alt.Axis(title=columns_stats[stats_type_index]),
                    scale=alt.Scale(domain=domain),
                ),
                y=alt.Y(
                    column_name,
                    type="nominal",
                    sort="-x",
                    axis=alt.Axis(title="", labelLimit=400),
                ),
                tooltip=[column_name, columns_stats[0], columns_stats[1]],
            )
            .properties(
                width="container", title=alt.TitleParams(text=title, anchor="start")
            )
            .interactive(),
            use_container_width=True,
        )


def show_counts_percent_grouped_chart(
    dset,
    title,
    column_names,
    columns_stats=None,
    stats_type="Percentages",
):
    """Draw a grouped distribution chart with counts and percentages.

    Args:
        dset (pandas.DataFrame): dataset
        column_stats (list): column names for the stats
        column_percent (str): column name for the percentages
        use_container_width (bool): use container width
    """

    if columns_stats is None:
        columns_stats = COLUMN_STATS

    stats_type_index = STATS_TYPES.index(stats_type)

    dset = dset[dset[columns_stats[0]] > 0]

    with st.container(border=True):
        st.altair_chart(
            alt.Chart(dset.reset_index())
            .mark_bar()
            .encode(
                x=alt.X(f"{columns_stats[stats_type_index]}:Q").title(""),
                y=alt.Y(f"{column_names[0]}:N").title(""),
                yOffset=f"{column_names[1]}:N",
                color=alt.Color(
                    f"{column_names[1]}:N",
                    scale=alt.Scale(),
                    legend=alt.Legend(
                        title="",
                        orient="top",
                        legendX=130,
                        legendY=40,
                        direction="horizontal",
                        titleAnchor="middle",
                    ),
                ),
                tooltip=[
                    column_names[0],
                    column_names[1],
                    columns_stats[0],
                    columns_stats[1],
                ],
            )
            .properties(
                width="container", title=alt.TitleParams(text=title, anchor="start")
            )
            .interactive(),
            use_container_width=True,
        )


def show_grouped_counts_chart(dset, x, y, colour):
    """Draw a chart with grouped counts.

    Args:
        dset (pandas.DataFrame): dataset
        x (str): column name for the x axis
        y (str): column name for the y axis
        colour (str): column name for the colour
    """

    # define the chart elements
    y_title = clean_titles(y)
    x_title = clean_titles(x)
    title = f"{y_title} by {x_title}"
    x = {
        "field": x,
        "type": "nominal",
        "axis": {"title": "", "labelLimit": 0, "labelAngle": 90},
    }
    y = {"field": y, "type": "nominal", "axis": {"title": "", "labelLimit": 0}}
    size = {"field": "records", "type": "quantitative"}
    color = {"field": colour, "type": "nominal", "legend": None}

    # add chart to display
    chart = {
        "title": {"text": title, "anchor": "middle"},
        "mark": {"type": "circle", "tooltip": True},
        "encoding": {"x": x, "y": y, "size": size, "color": color},
    }

    st.vega_lite_chart(dset, chart, use_container_width=True)


def display_description(description):
    """Display a description.

    Args:
        description (str): description
    """

    if description != "":
        if description.startswith(sh.PREFIX_WARNING):
            st.warning(description.replace(sh.PREFIX_WARNING, ""), icon="⚠️")
        else:
            st.markdown(description)


def display_added_columns(dset):
    """Display added columns.

    Args:
        dset (pandas.DataFrame): dataset
    """

    columns_added = [
        column
        for column in dset.columns
        if any(suffix in column for suffix in cb.ADDED_SUFFIXES)
    ]
    if len(columns_added) > 0:
        columns_added_to_print = []
        for column in columns_added:
            if column in cb.ADDED_DESCRIPTIONS:
                columns_added_to_print.append(
                    f"{column}: {cb.ADDED_DESCRIPTIONS[column]}"
                )
            else:
                columns_added_to_print.append(column)

        st.markdown(sh.ADDED_TITLE)
        stx.scrollableTextbox("\n".join(columns_added_to_print), key="stx_added")


def display_data_description(dset, description=""):
    """Display a description of the data.

    Args:
        dset (pandas.DataFrame): dataset
        logs (str): logs
        description (str): description
    """

    display_description(description)

    display_added_columns(dset)

    display_fields(dset)


def display_logs(logs):
    """Display logs.

    Args:
        logs (str): logs
    """

    stx.scrollableTextbox(logs, key="stx_logs")


def display_fields(dset):
    """Display fields.

    Args:
        dset (pandas.DataFrame): dataset
    """

    st.markdown(sh.FIELDS_TITLE)
    column_dtypes = [(column, str(dtype)) for column, dtype in dset.dtypes.items()]
    for [column_name, column_type] in column_dtypes:
        if column_type == "category":
            categories_count = dset[column_name].nunique()
            if categories_count > 1:
                categories_count_text = sh.CATEGORY_LABEL_PLURAL
            else:
                categories_count_text = sh.CATEGORY_LABEL_SINGULAR
            st.markdown(
                f"**{column_name}** - *{column_type}, "
                f"{categories_count} {categories_count_text}*"
            )
            if column_name not in cb.FIELDS_TO_NOT_DISPLAY:
                categories = "\n".join(sorted(dset[column_name].dropna().unique()))
                if categories_count > 1:
                    stx.scrollableTextbox(categories, key=f"stx_{column_name}")
                else:
                    with st.container(border=True):
                        st.markdown(categories)

        elif column_type in ["int64", "float64"]:
            column_type = "number"
            column_description = pd.DataFrame(
                data=[
                    dset[column_name]
                    .describe()
                    .loc[DESCRIPTION_MEASURES]
                    .round(0)
                    .astype(int)
                    .to_dict()
                ]
            )

            st.markdown(f"**{column_name}** - *{column_type}*")
            st.dataframe(column_description, hide_index=True)
        elif column_type in ["string", "object"]:
            st.markdown(f"**{column_name}** - *{sh.OBJECT_LABEL}*")
            if column_name not in cb.FIELDS_TO_NOT_DISPLAY:
                items = "\n".join(sorted(dset[column_name].dropna().unique()))
                stx.scrollableTextbox(items, key=f"stx_{column_name}")
        else:
            st.markdown(f"`{column_name}` ({column_type})")
            items = "\n".join(sorted(dset[column_name].dropna().unique()))
            stx.scrollableTextbox(items, key=f"stx_{column_name}")


def display_metrics(dset, labels=None):
    """Display metrics for a dataset.

    Args:
        dset (pandas.DataFrame): dataset
    """

    if labels is None:
        labels = [sh.RECORDS_LABEL, sh.INSTITUTIONS_LABEL]
    with st.container(border=True):
        cols = st.columns(2)
        cols[0].metric(label=labels[0], value=dset.shape[0])
        cols[1].metric(
            label=labels[1],
            value=dset[cb.COL_INST_NAME].nunique(),
        )


def display_dataframe(dset, data_prefix=""):
    """Display a dataframe.

    Args:
        dset (pandas.DataFrame): dataset
        data_prefix (str): data prefix
    """

    st.markdown(
        sh.BROWSE_DATA_TAB_DESCRIPTION.replace(
            sh.DATA_TEXT_TO_REPLACE, f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}"
        )
    )
    st.dataframe(dset, use_container_width=False)


def display_table_from_dictionary(dict_data):
    """Display a table from a dictionary.

    Args:
        dict (dict): dictionary
    """
    for items in dict_data.items():
        st.text(f"{items[0]} \t{items[1]}")


def display_distributions(dset, data_prefix="", key=None):
    """Display distributions for a selected column.

    Args:
        dset (pandas.DataFrame): dataset
        data_prefix (str): data prefix
        key (str): key
    """

    st.markdown(
        sh.DISTRIBUTIONS_TAB_DESCRIPTION.replace(
            sh.DATA_TEXT_TO_REPLACE, f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}"
        )
    )

    fields = proc.get_column_lists(dset, "category")

    # one-variable distribution
    st.divider()
    st.markdown(sh.ONE_VARIABLE_DISTRIBUTION_TITLE)
    cols = st.columns(2)
    with cols[0]:
        column_to_plot = st.selectbox(
            sh.DISTRIBUTION_SELECT_PROMPT, fields, key=f"select_{key}_one", index=None
        )
    if column_to_plot:
        with cols[1]:
            stats_type_one_var = st.radio(
                sh.SELECT_STATS_PROMPT,
                options=STATS_TYPES,
                index=0,
                horizontal=True,
                key=f"radio_{key}_{column_to_plot}",
            )

        dset_stats_one_var = proc.calculate_counts(dset, column_to_plot, sort=True)

        show_counts_percent_chart(
            dset_stats_one_var,
            f"{clean_titles(column_to_plot)} "
            f"(N = {dset.shape[0]}{data_prefix} records)",
            column_to_plot,
            stats_type=stats_type_one_var,
        )

    # two-variable distribution
    st.divider()
    st.markdown(sh.TWO_VARIABLE_DISTRIBUTION_TITLE)
    cols = st.columns(3)
    with cols[0]:
        column_one_to_plot = st.selectbox(
            sh.DISTRIBUTION_SELECT_PROMPT_1, fields, key=f"select_{key}_two_1", index=None
        )
    if column_one_to_plot:
        fields_2 = [field for field in fields if field != column_one_to_plot]
        with cols[1]:
            column_two_to_plot = st.selectbox(
                sh.DISTRIBUTION_SELECT_PROMPT_2,
                fields_2,
                key=f"select_{key}_two_2",
                index=None,
            )
        if column_two_to_plot:
            with cols[2]:
                stats_type_two_vars = st.radio(
                    sh.SELECT_STATS_PROMPT,
                    options=STATS_TYPES,
                    index=0,
                    horizontal=True,
                    key=f"radio_{key}_{column_one_to_plot}_{column_two_to_plot}",
                )
            dset_stats_two_vars = proc.calculate_grouped_counts(
                dset, [column_one_to_plot, column_two_to_plot]
            )
            show_counts_percent_grouped_chart(
                dset_stats_two_vars,
                f"{clean_titles(column_one_to_plot)} by {clean_titles(column_two_to_plot)} "
                f"(N = {dset.shape[0]}{data_prefix} records)",
                [
                    column_one_to_plot,
                    column_two_to_plot,
                ],
                columns_stats=None,
                stats_type=stats_type_two_vars,
            )


def display_histograms(dset, data_prefix="", key=None):
    """Display histograms for a selected column.

    Args:
        dset (pandas.DataFrame): dataset
    """

    fields = proc.get_column_lists(dset, "number")
    nrecords = dset.shape[0]
    column_selected = st.selectbox(
        sh.DISTRIBUTION_SELECT_PROMPT, fields, key=key, index=0
    )
    cols = st.columns(2)
    with cols[0]:
        stats_type = st.radio(
            sh.SELECT_STATS_PROMPT,
            options=STATS_TYPES,
            index=0,
            horizontal=True,
            key=f"radio_{key}_{column_selected}",
        )
    with cols[1]:
        bins = st.select_slider(
            sh.BIN_NUMBER_PROMPT,
            options=BIN_OPTIONS,
            value=10,
            key=f"slider_bins_{key}_{column_selected}",
        )
    if column_selected:
        dset_temp = pd.cut(dset[column_selected], bins).apply(
            lambda x: pd.Interval(
                int(round(x.left)), int(round(x.right)), closed="right"
            )
        )
        dset_plot = dset_temp.value_counts(normalize=False).to_frame(
            name=COLUMN_STATS[0]
        )
        dset_plot = dset_plot.merge(
            dset_temp.value_counts(normalize=True).to_frame(name=COLUMN_STATS[1]),
            how="left",
            left_index=True,
            right_index=True,
        )
        dset_plot[COLUMN_STATS[1]] = np.round(dset_plot[COLUMN_STATS[1]] * 100)
        dset_plot.index.name = column_selected
        dset_plot.index = dset_plot.index.astype(str)

        with st.container(border=True):
            show_counts_percent_chart(
                dset_plot,
                f"{column_selected} (N = {nrecords} {data_prefix} records)",
                column_selected,
                stats_type=stats_type,
            )


def display_grouped_distribution(dset, key=None):
    """Display a grouped distribution for a selected column.

    Args:
        dset (pandas.DataFrame): dataset
    """
    fields = proc.get_column_lists(dset, "category")
    columns_to_plot = st.multiselect(
        sh.GROUPED_DISTRIBUTION_SELECT_PROMPT,
        fields,
        max_selections=2,
        key=key,
        default=None,
    )
    if len(columns_to_plot) == 2:
        dset_stats = proc.calculate_grouped_counts(dset, columns_to_plot)
        with chart_container(dset_stats, export_formats=sh.DATA_EXPORT_FORMATS):
            show_grouped_counts_chart(
                dset_stats, columns_to_plot[0], columns_to_plot[1], columns_to_plot[0]
            )


def display_data_explorer(dset, key=None, do_histograms=False):
    """Display a data explorer for a selected dataset.

    Args:
        dset (pandas.DataFrame): dataset
    """

    with st.container(border=True):
        st.markdown(sh.DATA_EXPLORER_DESCRIPTION)
        dset_explore = dataframe_explorer(dset)

        if dset_explore.shape[0] == 0:
            st.warning(sh.NO_SELECTED_RECORDS_WARNING)
        else:
            data_prefix = ""
            if dset_explore.shape[0] < dset.shape[0]:
                data_prefix = " selected"
                labels = [
                    f"{sh.SELECTED_LABEL} {sh.RECORDS_LABEL.lower()}",
                    f"{sh.SELECTED_LABEL} {sh.INSTITUTIONS_LABEL.lower()}",
                ]
                display_metrics(dset_explore, labels=labels)

            tabs = st.tabs(
                [
                    sh.VISUALISE_TAB_HEADER.replace(
                        sh.DATA_TEXT_TO_REPLACE,
                        f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}",
                    ),
                    sh.SHOW_TAB_HEADER.replace(
                        sh.DATA_TEXT_TO_REPLACE,
                        f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}",
                    ),
                ]
            )
            with tabs[0]:
                if not do_histograms:
                    display_distributions(
                        dset_explore, data_prefix=data_prefix, key=key
                    )
                else:
                    vtabs = st.tabs(
                        [sh.DISTRIBUTIONS_TAB_HEADER, sh.HISTOGRAMS_TAB_HEADER]
                    )
                    with vtabs[0]:
                        display_distributions(
                            dset_explore, data_prefix=data_prefix, key=key
                        )
                    with vtabs[1]:
                        display_histograms(
                            dset_explore, data_prefix=data_prefix, key="histograms"
                        )
            with tabs[1]:
                display_dataframe(dset_explore, data_prefix=data_prefix)
