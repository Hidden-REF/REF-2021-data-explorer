""" Visualisation functions. """
import streamlit as st
import altair as alt

import read_write as rw


USE_CONTAINER_WIDTH = True


def draw_counts_percent_chart(dset,
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
                    ).interactive()
    st.altair_chart(chart,
                    use_container_width=USE_CONTAINER_WIDTH)
    rw.download_data(dset,
                     "Download chart data as csv",
                     "chart_data.csv")


def draw_grouped_counts_chart(dset, x, y, colour):
    """ Draw a chart with grouped counts.

        Args:
            dset (pandas.DataFrame): dataset
            x (str): column name for the x axis
            y (str): column name for the y axis
            colour (str): column name for the colour
    """
    st.vega_lite_chart(dset, {
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
                              'type': 'quantitative',
                              'legend': None},
                     'color': {'field': colour,
                               'type': 'nominal',
                               'legend': None}}
        }, use_container_width=True)
