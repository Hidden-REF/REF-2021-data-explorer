import pandas as pd
import streamlit as st

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis


page_title = "Outputs"
st.title(page_title)

with st.spinner(rw.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_OUTPUTS)

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

st.subheader("Charts")
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
            vis.draw_counts_percent_chart(dset_stats,
                                          column)


with tab2:
    search_type = st.selectbox("Select an output type to display",
                               [""] + list(cb.OUTPUT_TYPE_NAMES.values()),
                               index=0
                               )

    if search_type:
        with st.spinner(rw.PROC_TEXT):
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
        with st.spinner(rw.PROC_TEXT):
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
                vis.draw_counts_percent_chart(dset_stats,
                                              column)
