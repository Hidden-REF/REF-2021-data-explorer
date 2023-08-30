import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.chart_container import chart_container

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis
import shared as sh

STRING_COLUMNS = [cb.COL_OUTPUT_TITLE,
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
                  cb.COL_OUTPUT_SUPP]

CATEGORIES_COLUMNS = [cb.COL_OUTPUT_TYPE_NAME,
                      cb.COL_OUTPUT_CITATIONS,
                      cb.COL_OUTPUT_INTERDISCIPLINARY,
                      cb.COL_OUTPUT_NON_ENGLISH,
                      cb.COL_OUTPUT_FORENSIC_SCIENCE,
                      cb.COL_OUTPUT_CRIMINOLOGY,
                      cb.COL_OUTPUT_DOUBLE_WEIGHTING,
                      cb.COL_OUTPUT_RESERVE_OUTPUT,
                      cb.COL_OPEN_ACCESS,
                      cb.COL_OUTPUT_DELAYED]

page_title = "Outputs"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_OUTPUTS,
                            categories_columns=CATEGORIES_COLUMNS,
                            string_columns=STRING_COLUMNS)

vis.display_record_counts_table(dset)

# distribution charts
# -------------------
st.subheader(sh.CHARTS_HEADER)
dcolumns = [cb.COL_PANEL_NAME,
            cb.COL_UOA_NAME,
            cb.COL_OUTPUT_TYPE_NAME,
            cb.COL_OUTPUT_INTERDISCIPLINARY,
            cb.COL_OPEN_ACCESS]
dtabs = st.tabs(dcolumns)

for i, column in enumerate(dcolumns):
    with dtabs[i]:
        dset_stats = proc.calculate_counts(dset,
                                           column,
                                           sort=False)
        with chart_container(dset_stats):
            vis.draw_counts_percent_chart(dset_stats,
                                          column)

# select categorical values and export
# ------------------------------------
st.divider()
st.markdown(f"## {sh.SELECT_EXPORT_HEADER_PREFIX} ...")

scolumns = dcolumns.copy()
stabs = st.tabs(scolumns)

for i, column in enumerate(scolumns):
    with stabs[i]:
        options = list(dset[column].cat.categories)
        prompt = f"##### Select `{column}` value"
        option = st.selectbox(prompt,
                              [""] + options,
                              index=0,
                              help="Select a value to filter the data")

        if option:
            with st.spinner(sh.PROC_TEXT):
                dset_selected = dset[dset[column] == option]
            dict = {"Selected": option,
                    "Records": dset_selected.shape[0]}
            vis.display_table_from_dictionary(dict)
            rw.download_data(dset_selected,
                             sh.DOWNLOAD_SELECTED_DATA_PROMPT,
                             "selected_data.csv")

# search string fields for pattern
# --------------------------------
st.divider()
st.markdown(f"## {sh.SEARCH_EXPORT_HEADER_PREFIX} ...")
pcolumns = [cb.COL_OUTPUT_TITLE]

ptabs = st.tabs(pcolumns)

for i, column in enumerate(pcolumns):
    with ptabs[i]:
        prompt = f"Enter a pattern to search '{column}'"
        pattern = st.text_input(prompt,
                                max_chars=40,
                                value="",
                                help="Enter a pattern to search for"
                                )
        if pattern:
            with st.spinner(sh.PROC_TEXT):
                dset_selected = dset[dset[column].str.contains(pattern,
                                                               case=False,
                                                               na=False)]
            dict = {"Pattern": pattern,
                    "Records": dset_selected.shape[0]}
            vis.display_table_from_dictionary(dict)
            rw.download_data(dset_selected,
                             sh.DOWNLOAD_SELECTED_DATA_PROMPT,
                             "selected_data.csv")

# explore data
# ------------
st.divider()
st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
st.dataframe(dset_explore, use_container_width=False)
