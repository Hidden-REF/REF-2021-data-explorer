import pandas as pd
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.chart_container import chart_container

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis
import shared as sh


page_title = "Outputs"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_OUTPUTS,
                            categories_columns=[cb.COL_OUTPUT_TYPE_NAME,
                                                cb.COL_OUTPUT_CITATIONS,
                                                cb.COL_OUTPUT_INTERDISCIPLINARY,
                                                cb.COL_OUTPUT_NON_ENGLISH,
                                                cb.COL_OUTPUT_FORENSIC_SCIENCE,
                                                cb.COL_OUTPUT_CRIMINOLOGY,
                                                cb.COL_OUTPUT_DOUBLE_WEIGHTING,
                                                cb.COL_OUTPUT_RESERVE_OUTPUT,
                                                cb.COL_OPEN_ACCESS,
                                                cb.COL_OUTPUT_DELAYED],
                            string_columns=[cb.COL_OUTPUT_TITLE,
                                            cb.COL_OUTPUT_RG_NAME,
                                            cb.COL_OUTPUT_PLACE,
                                            cb.COL_OUTPUT_PUBLISHER,
                                            cb.COL_OUTPUT_VOL_TITLE,
                                            cb.COL_OUTPUT_VOL_NO,
                                            cb.COL_OUTPUT_ISSUE,
                                            cb.COL_OUTPUT_FIRST_PAGE,
                                            cb.COL_OUTPUT_ARTICLE_NO,
                                            cb.COL_OUTPUT_ISBN,
                                            cb.COL_OUTPUT_ISSN,
                                            cb.COL_OUTPUT_DOI,
                                            cb.COL_OUTPUT_PATENT_NO,
                                            cb.COL_OUTPUT_MONTH,
                                            cb.COL_OUTPUT_URL,
                                            cb.COL_OUTPUT_SUPP])


dset_to_print = pd.DataFrame.from_dict(
    {
        "Outputs records": dset.shape[0],
        "Institutions": dset[cb.COL_INST_NAME].nunique()
    },
    orient="index"
    )
dset_to_print.columns = ["count"]
pd.set_option("display.max_colwidth", None)
st.dataframe(dset_to_print)

st.subheader(sh.CHARTS_HEADER)

tab1, tab2, tab3 = st.tabs(["All records", "Explore types", "Search titles"])

with tab1:
    st.markdown("Select from the charts below to view the "
                "distributions for the number of outputs records by ...")
    columns = [cb.COL_PANEL_NAME,
               cb.COL_UOA_NAME,
               cb.COL_OUTPUT_TYPE_NAME,
               cb.COL_OUTPUT_INTERDISCIPLINARY,
               cb.COL_OPEN_ACCESS]
    tabs = st.tabs(columns)
    for i, column in enumerate(columns):
        with tabs[i]:
            dset_stats = proc.calculate_counts(dset,
                                               column,
                                               sort=False)
            with chart_container(dset_stats):
                vis.draw_counts_percent_chart(dset_stats,
                                              column)


with tab2:
    output_names = cb.enum_values[cb.COL_OUTPUT_TYPE_NAME]
    search_type = st.selectbox("Select an output type to display",
                               [""] + list(output_names.values()),
                               index=0
                               )

    if search_type:
        with st.spinner(sh.PROC_TEXT):
            dset_selected = dset[dset[cb.COL_OUTPUT_TYPE_NAME] == search_type]
        st.markdown(f"Number of outputs records of type '{search_type}': "
                    f"{dset_selected.shape[0]}")
        rw.download_data(dset_selected,
                         f"Download '{search_type}' outputs as csv",
                         "selected_data.csv")

        st.markdown("Select from the charts below to view the "
                    "distributions for the number of selected outputs records by ...")
        columns = [cb.COL_PANEL_NAME,
                   cb.COL_UOA_NAME,
                   cb.COL_OUTPUT_INTERDISCIPLINARY,
                   cb.COL_OPEN_ACCESS]
        tabs = st.tabs(columns)
        for i, column in enumerate(columns):
            with tabs[i]:
                dset_stats = proc.calculate_counts(dset_selected,
                                                   column,
                                                   sort=False)
                with chart_container(dset_stats):
                    vis.draw_counts_percent_chart(dset_stats,
                                                  column)

with tab3:
    search_word = st.text_input(f"Enter a term to search the '{cb.COL_OUTPUT_TITLE}'"
                                " of the outputs,"
                                " for example software,"
                                " computation, database, machine learning etc.",
                                max_chars=40,
                                value="",
                                help="Enter a term to search for."
                                )
    search_column = cb.COL_OUTPUT_TITLE
    if search_word:
        with st.spinner(sh.PROC_TEXT):
            dset_selected = dset[dset[search_column].str.contains(search_word,
                                                                  case=False,
                                                                  na=False)]
        st.markdown(f"Number of outputs records with '{search_word}' in '{search_column}': "
                    f"{dset_selected.shape[0]}")

        rw.download_data(dset_selected,
                         f"Download outputs with '{search_word}' in '{search_column}' as csv",
                         "selected_data.csv")

        st.markdown("Select from the charts below to view the "
                    "distributions for the number of selected outputs records by ...")
        columns = [cb.COL_PANEL_NAME,
                   cb.COL_UOA_NAME,
                   cb.COL_OUTPUT_TYPE_NAME,
                   cb.COL_OUTPUT_INTERDISCIPLINARY,
                   cb.COL_OPEN_ACCESS]
        tabs = st.tabs(columns)
        for i, column in enumerate(columns):
            with tabs[i]:
                dset_stats = proc.calculate_counts(dset_selected,
                                                   column,
                                                   sort=False)
                with chart_container(dset_stats):
                    vis.draw_counts_percent_chart(dset_stats,
                                                  column)

st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
st.dataframe(dset_explore, use_container_width=False)
