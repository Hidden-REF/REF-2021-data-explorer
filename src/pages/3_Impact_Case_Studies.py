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
        with chart_container(dset_stats, export_formats=sh.DATA_EXPORT_FORMATS):
            vis.draw_counts_percent_chart(dset_stats,
                                          column)

# explore data
# ------------
st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
if (dset_explore.shape[0] < dset.shape[0]) & (dset_explore.shape[0] > 0):
    dict = {"Selected records": dset_explore.shape[0]}
    vis.display_table_from_dictionary(dict)
    rw.download_data(dset_explore,
                     sh.DOWNLOAD_SELECTED_DATA_PROMPT,
                     "selected_data.csv")
    st.dataframe(dset_explore, use_container_width=False)
