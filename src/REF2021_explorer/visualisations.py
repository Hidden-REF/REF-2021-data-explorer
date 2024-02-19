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

STATS_TYPES = ["Percentages", "Counts"]

COLUMN_STATS = ["records", "records (%)"]

DESCRIPTION_MEASURES = ["min", "max", "mean", "std"]

BIN_OPTIONS = [5, 10, 25, 50, 75, 100, 125, 150, 175, 200, 250, 300]


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

    # define the chart elements
    title = alt.TitleParams(text=title, anchor="start", fontSize=14, dy=-10)
    if stats_type == STATS_TYPES[1]:
        # counts
        x = alt.X(
            columns_stats[0], type="quantitative", axis=alt.Axis(title=columns_stats[0])
        )
    else:
        # percentages
        x = alt.X(
            columns_stats[1],
            type="quantitative",
            axis=alt.Axis(title=columns_stats[1]),
            scale=alt.Scale(domain=[0, 100]),
        )

    y = alt.Y(
        column_name, type="nominal", sort="-x", axis=alt.Axis(title="", labelLimit=400)
    )

    tooltip = [column_name, columns_stats[0], columns_stats[1]]

    # add chart to display
    chart = (
        alt.Chart(dset.reset_index())
        .mark_bar()
        .encode(x=x, y=y, tooltip=tooltip)
        .properties(title=title)
        .interactive()
    ).properties(width="container")

    with st.container(border=True):
        st.altair_chart(chart, use_container_width=True)


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

    st.markdown(sh.BROWSE_DATA_TAB_DESCRIPTION.replace(
                        sh.DATA_TEXT_TO_REPLACE, f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}"
                    ))
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

    st.markdown(sh.DISTRIBUTIONS_TAB_DESCRIPTION.replace(
                        sh.DATA_TEXT_TO_REPLACE, f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}"
                    ))

    fields = proc.get_column_lists(dset, "category")

    cols = st.columns(2)
    with cols[0]:
        column_to_plot = st.selectbox(
            sh.DISTRIBUTION_SELECT_PROMPT, fields, key=key, index=0
        )
    with cols[1]:
        stats_type = st.radio(
            sh.SELECT_STATS_PROMPT,
            options=STATS_TYPES,
            index=0,
            horizontal=True,
            key=f"radio_{key}_{column_to_plot}",
        )
    if column_to_plot:
        dset_stats = proc.calculate_counts(dset, column_to_plot, sort=True)

        show_counts_percent_chart(
            dset_stats,
            f"{clean_titles(column_to_plot)} " f"(N = {dset.shape[0]}{data_prefix} records)",
            column_to_plot,
            stats_type=stats_type,
        )


def display_histograms(dset, key=None):
    """Display histograms for a selected column.

    Args:
        dset (pandas.DataFrame): dataset
    """

    fields = proc.get_column_lists(dset, "number")
    nrecords = dset.shape[0]
    column_selected = st.selectbox(
        sh.DISTRIBUTION_SELECT_PROMPT, fields, key=key, index=0
    )
    if column_selected:
        nnegative = dset[dset[column_selected] < 0].shape[0]
        cols = st.columns(2)
        with cols[0]:
            bins = st.select_slider(
                sh.BIN_NUMBER_PROMPT,
                options=BIN_OPTIONS,
                value=10,
                key=f"slider_bins_{key}_{column_selected}",
            )
        with cols[1]:
            stats_type = st.radio(
                sh.SELECT_STATS_PROMPT,
                options=STATS_TYPES,
                index=0,
                horizontal=True,
                key=f"radio_{key}_{column_selected}",
            )
            if nnegative > 0:
                exclude_negative = st.toggle(
                    sh.EXCLUDE_NEGATIVE_PROMPT,
                    value=False,
                    key=f"toggle_{key}_{column_selected}",
                )
            else:
                exclude_negative = False
        min_max = [
            int(np.ceil(dset[column_selected].min())),
            int(np.floor(dset[column_selected].max())),
        ]
        if exclude_negative:
            min_max[0] = 0
        limits = st.slider(
            sh.SELECT_DATA_RANGE_PROMPT,
            min_max[0],
            min_max[1],
            min_max,
            key=f"slider_limits_{key}_{column_selected}",
        )
        if bins:
            indices_selected = (dset[column_selected] >= limits[0]) & (
                dset[column_selected] <= limits[1]
            )
            nselected = dset[indices_selected].shape[0]
            hcounts, bin_edges = np.histogram(
                dset.loc[indices_selected, column_selected], bins=bins
            )
            x_limits = [min(bin_edges), max(bin_edges)]
            hpercs = np.round(100 * hcounts / hcounts.sum(), 0)
            bin_edges = np.round(bin_edges).astype(int)
            bin_labels = [
                f"{bin_edges[i]} to {bin_edges[i+1]}" for i in range(len(bin_edges) - 1)
            ]
            column_x = "value"
            column_label = "Interval"
            column_counts = STATS_TYPES[1][:-1]
            column_percs = STATS_TYPES[0][:-1]
            dset_plot = pd.DataFrame.from_dict(
                {
                    column_label: bin_labels,
                    column_counts: hcounts,
                    column_percs: hpercs,
                }
            )
            dset_plot.set_index(column_label, inplace=True)
            with chart_container(dset_plot, export_formats=sh.DATA_EXPORT_FORMATS):
                # define the chart elements
                dset_to_plot = dset_plot.copy()
                dset_to_plot[column_x] = bin_edges[:-1]

                title_text = f"{column_selected}: {nselected} of {nrecords} records"
                x = alt.X(
                    column_x,
                    type="quantitative",
                    axis=alt.Axis(title=""),
                    scale=alt.Scale(domain=x_limits),
                )
                y = alt.Y(
                    stats_type[:-1],
                    type="quantitative",
                    axis=alt.Axis(title=stats_type, labelLimit=400),
                    sort="y",
                )
                tooltip = [column_label, column_counts, column_percs]
                title = alt.TitleParams(
                    text=title_text, anchor="middle", fontSize=14, dy=-10
                )
                # add chart to display
                chart = (
                    alt.Chart(dset_to_plot.reset_index())
                    .mark_bar()
                    .encode(x=x, y=y, tooltip=tooltip)
                    .properties(title=title)
                    .interactive()
                )
                st.altair_chart(chart, use_container_width=USE_CONTAINER_WIDTH)


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


def display_data_explorer(dset, do_histograms=False):
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
                    sh.SHOW_TAB_HEADER.replace(
                        sh.DATA_TEXT_TO_REPLACE, f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}"
                    ),
                    sh.VISUALISE_TAB_HEADER.replace(
                        sh.DATA_TEXT_TO_REPLACE, f"{data_prefix}{sh.DATA_TEXT_TO_REPLACE}"),
                ]
            )
            with tabs[0]:
                display_dataframe(dset_explore, data_prefix=data_prefix)
            with tabs[1]:
                display_distributions(dset_explore, data_prefix=data_prefix, key="distributions")

                if do_histograms:
                    display_histograms(dset_explore, key="h_selected")