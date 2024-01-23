import streamlit as st

import codebook as cb
import read_write as rw
import visualisations as vis
import shared as sh


CATEGORIES_COLUMNS = [cb.COL_INCOME_SOURCE,
                      cb.COL_MULT_SUB_LETTER,
                      cb.COL_MULT_SUB_NAME,
                      cb.COL_JOINT_SUB]
DROP_COLUMNS = [cb.COL_INST_CODE]

st.title(sh.RESEARCH_INCOME_IN_KIND_TITLE)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_RINCOMEINKIND,
                            categories_columns=CATEGORIES_COLUMNS,
                            drop_columns=DROP_COLUMNS)

vis.display_record_counts_table(dset)

with st.expander(sh.VISUALISE_HEADER):
    tabs = st.tabs([sh.DISTRIBUTIONS_TAB_HEADER,
                    sh.GROUPED_DISTRIBUTIONS_TAB_HEADER,
                    sh.HISTOGRAMS_TAB_HEADER])
    with tabs[0]:
        vis.display_distributions(dset)
    with tabs[1]:
        vis.display_grouped_distribution(dset)
    with tabs[2]:
        vis.display_histograms(dset)
with st.expander(sh.EXPLORE_HEADER):
    vis.display_data_explorer(dset, do_histograms=True)
