import streamlit as st

import codebook as cb
import read_write as rw
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

CATEGORIES_COLUMNS = [cb.COL_MULT_SUB_LETTER,
                      cb.COL_MULT_SUB_NAME,
                      cb.COL_JOINT_SUB,
                      cb.COL_OUTPUT_TYPE_NAME,
                      cb.COL_OUTPUT_CITATIONS,
                      cb.COL_OUTPUT_INTERDISCIPLINARY,
                      cb.COL_OUTPUT_NON_ENGLISH,
                      cb.COL_OUTPUT_FORENSIC_SCIENCE,
                      cb.COL_OUTPUT_CRIMINOLOGY,
                      cb.COL_OUTPUT_DOUBLE_WEIGHTING,
                      cb.COL_OUTPUT_RESERVE_OUTPUT,
                      cb.COL_OPEN_ACCESS,
                      cb.COL_OUTPUT_DELAYED]
DROP_COLUMNS = [cb.COL_INST_CODE]

st.title(sh.OUTPUTS_TITLE)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_OUTPUTS,
                            categories_columns=CATEGORIES_COLUMNS,
                            string_columns=STRING_COLUMNS,
                            drop_columns=DROP_COLUMNS)

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
