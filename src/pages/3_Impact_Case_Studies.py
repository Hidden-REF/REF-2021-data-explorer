import streamlit as st

import codebook as cb
import read_write as rw
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

st.title(sh.IMPACT_CASE_STUDIES_TITLE)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_IMPACTS,
                            categories_columns=CATEGORIES_COLUMNS,
                            string_columns=STRING_COLUMNS)

vis.display_record_counts_table(dset)
with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER,
                    sh.GROUPED_DISTRIBUTIONS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)
    with tabs[1]:
        vis.display_grouped_distribution(dset)
with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset)
