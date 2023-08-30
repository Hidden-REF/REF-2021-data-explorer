import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.chart_container import chart_container

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis
import shared as sh

STRING_COLUMNS = [cb.COL_IMPACT_TITLE,
                  cb.COL_IMPACT_COUNTRIES,
                  cb.COL_IMPACT_FORMAL_PARTNERS,
                  cb.COL_IMPACT_FUNDING_PROGS,
                  cb.COL_IMPACT_GLOBAL_RID,
                  cb.COL_IMPACT_FUNDERS_NAME,
                  cb.COL_IMPACT_ORCIDs,
                  cb.COL_IMPACT_GRANT_FUNDING,
                  cb.COL_IMPACT_SUMMARY,
                  cb.COL_IMPACT_UNDERPIN_RESEARCH,
                  cb.COL_IMPACT_REFERENCES_RESEARCH,
                  cb.COL_IMPACT_DETAILS,
                  cb.COL_IMPACT_CORROBORATE]
CATEGORIES_COLUMNS = [cb.COL_IMPACT_CONTINUED]

page_title = "Impact Case Studies"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_IMPACTS,
                            categories_columns=CATEGORIES_COLUMNS,
                            string_columns=STRING_COLUMNS)
print(dset.columns)

vis.display_record_counts_table(dset)

# distribution charts
# -------------------
st.subheader(sh.CHARTS_HEADER)
dcolumns = [cb.COL_PANEL_NAME,
            cb.COL_UOA_NAME,
            cb.COL_IMPACT_CONTINUED]
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
pcolumns = [cb.COL_IMPACT_TITLE,
            cb.COL_IMPACT_SUMMARY,
            cb.COL_IMPACT_UNDERPIN_RESEARCH,
            cb.COL_IMPACT_REFERENCES_RESEARCH,
            cb.COL_IMPACT_DETAILS]

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
