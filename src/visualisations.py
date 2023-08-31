""" Visualisation functions. """
import pandas as pd
import streamlit as st
from streamlit_extras.chart_container import chart_container
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.grid import grid
import plotly.figure_factory as ff


import altair as alt

import codebook as cb
import process as proc
import shared as sh


USE_CONTAINER_WIDTH = True


def show_counts_percent_chart(dset,
                              column_name,
                              column_count="records",
                              column_percent="records (%)",
                              use_container_width=USE_CONTAINER_WIDTH
                              ):
    """ Draw a chart with counts and percentages.

        Args:
            dset (pandas.DataFrame): dataset
            column_name (str): column name
            column_count (str): column name for the counts
            column_percent (str): column name for the percentages
            use_container_width (bool): use container width
    """
    title = column_name.replace(" stars", "* rating")\
                       .replace(" star", "* rating")\
                       .replace(" (binned)", "")
    chart = alt.Chart(dset.reset_index())\
               .mark_bar()\
               .encode(
                        x=alt.X(column_percent,
                                type="quantitative",
                                axis=alt.Axis(title=column_percent),
                                scale=alt.Scale(domain=[0, 100])
                                ),
                        y=alt.Y(column_name,
                                type="nominal",
                                axis=alt.Axis(title="",
                                              labelLimit=400),
                                sort="y"
                                ),
                        tooltip=[column_name, column_count, column_percent],
                    ).properties(title=alt.TitleParams(text=title,
                                                       anchor="middle",
                                                       fontSize=14,
                                                       dy=-10
                                                       )
                                 ).interactive()
    st.altair_chart(chart,
                    use_container_width=USE_CONTAINER_WIDTH)


def show_grouped_counts_chart(dset, x, y, colour):
    """ Draw a chart with grouped counts.

        Args:
            dset (pandas.DataFrame): dataset
            x (str): column name for the x axis
            y (str): column name for the y axis
            colour (str): column name for the colour
    """
    st.vega_lite_chart(dset, {
        'title': {'text': f"{y} by {x}", 'anchor': 'middle'},
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {'x': {'field': x,
                           'type': 'nominal',
                           'axis': {'title': "",
                                    'labelLimit': 0,
                                    'labelAngle': 90
                                    }},
                     'y': {'field': y,
                           'type': 'nominal',
                           'axis': {'title': "",
                                    'labelLimit': 0}},
                     'size': {'field': 'records',
                              'type': 'quantitative'},
                     'color': {'field': colour,
                               'type': 'nominal',
                               'legend': None}}
        }, use_container_width=True)


def display_record_counts_table(dset):
    """ Display a table with the number of records and institutions.

        Args:
            dset (pandas.DataFrame): dataset
    """
    dset_to_print = pd.DataFrame.from_dict(
        {
            "Records": dset.shape[0],
            "Institutions": dset[cb.COL_INST_NAME].nunique()
        },
        orient="index")

    dset_to_print.columns = ["count"]
    pd.set_option("display.max_colwidth", None)
    st.dataframe(dset_to_print)


def display_table_from_dictionary(dict):
    """ Display a table from a dictionary.

        Args:
            dict (dict): dictionary
    """
    for items in dict.items():
        st.text(f"{items[0]} \t{items[1]}")


def display_distributions(dset, key=None):
    """ Display distributions for a selected column.

        Args:
            dset (pandas.DataFrame): dataset
    """
    fields = proc.get_column_lists(dset, "category")
    column_to_plot = st.selectbox(sh.DISTRIBUTION_SELECT_PROMPT,
                                  fields,
                                  key=key,
                                  index=0)
    if column_to_plot:
        dset_stats = proc.calculate_counts(dset, column_to_plot, sort=False)
        with chart_container(dset_stats, export_formats=sh.DATA_EXPORT_FORMATS):
            show_counts_percent_chart(dset_stats,
                                      column_to_plot)


def display_histograms(dset, key=None):
    fields = proc.get_column_lists(dset, "number")
    column_to_plot = st.selectbox(sh.DISTRIBUTION_SELECT_PROMPT,
                                  fields,
                                  key=key,
                                  index=0)
    if column_to_plot:
        min_bins = 25
        min_steps = 10
        min_value = 1
        max_value = (dset[column_to_plot].max() - dset[column_to_plot].min())/min_bins
        max_value = max_value.astype(int)
        step = (max_value - min_value)/min_steps
        step = step.astype(int)
        if (step == 0) | (min_value == 0) | (max_value <= 1) | (min_value == max_value):
            st.warning(sh.NOT_SUITABLE_FOR_HISTOGRAM_WARNING)
        else:
            bin_size = st.slider(sh.BIN_SIZE_PROMPT,
                                 key=f"{key}_{column_to_plot}",
                                 min_value=min_value,
                                 max_value=max_value,
                                 value=min_value,
                                 step=step)
            fig = ff.create_distplot([dset[column_to_plot]],
                                     [column_to_plot],
                                     histnorm="probability",
                                     show_rug=True,
                                     show_curve=False,
                                     bin_size=bin_size)
            fig.update_layout(showlegend=False,
                              title=column_to_plot,
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)


def display_grouped_distribution(dset, key=None):
    """ Display a grouped distribution for a selected column.

        Args:
            dset (pandas.DataFrame): dataset
    """
    fields = proc.get_column_lists(dset, "category")
    columns_to_plot = st.multiselect(sh.GROUPED_DISTRIBUTION_SELECT_PROMPT,
                                     fields,
                                     max_selections=2,
                                     key=key,
                                     default=None)
    if len(columns_to_plot) == 2:
        dset_stats = proc.calculate_grouped_counts(dset, columns_to_plot)
        with chart_container(dset_stats, export_formats=sh.DATA_EXPORT_FORMATS):
            show_grouped_counts_chart(dset_stats,
                                      columns_to_plot[0],
                                      columns_to_plot[1],
                                      columns_to_plot[0])


def display_data_explorer(dset, do_histograms=False):
    """ Display a data explorer for a selected dataset.

        Args:
            dset (pandas.DataFrame): dataset
    """
    dset_explore = dataframe_explorer(dset)
    if dset_explore.shape[0] < dset.shape[0]:
        if dset_explore.shape[0] == 0:
            st.warning(sh.NO_SELECTED_RECORDS_WARNING)
        else:
            g = grid(2, vertical_align="center")
            g.text(f"Selected records: {dset_explore.shape[0]}")
            g.download_button(
                label=sh.DOWNLOAD_SELECTED_DATA_BUTTON,
                data=dset_explore.to_csv().encode('utf-8'),
                file_name="selected_data.csv",
                mime='text/csv',
            )
            tabs = st.tabs([sh.SHOW_SELECTED_TAB_HEADER,
                            sh.VISUALISE_SELECTED_TAB_HEADER])
            with tabs[0]:
                st.dataframe(dset_explore, use_container_width=False)
            with tabs[1]:
                tabs_list = [sh.DISTRIBUTIONS_TAB_HEADER,
                             sh.GROUPED_DISTRIBUTIONS_TAB_HEADER]
                if do_histograms:
                    tabs_list.append(sh.HISTOGRAMS_TAB_HEADER)
                tabs = st.tabs(tabs_list)
                with tabs[0]:
                    display_distributions(dset_explore, key="d_selected")
                with tabs[1]:
                    display_grouped_distribution(dset_explore, key="g_selected")
                if do_histograms:
                    with tabs[2]:
                        display_histograms(dset_explore, key="h_selected")
