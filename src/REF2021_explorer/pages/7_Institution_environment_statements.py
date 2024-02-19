# pylint: disable=C0103
# pylint: disable=R0801
# pylint: disable=E0401
""" Institution environment statements page """
import streamlit as st
import fastparquet as fp
import duckdb

import REF2021_explorer.codebook as cb
import REF2021_explorer.read_write as rw
import REF2021_explorer.visualisations as vis
import REF2021_explorer.shared_content as sh


PAGE = "inst_env_statements"

sh.page_config(PAGE)
sh.sidebar_settings()
sh.sidebar_content(PAGE)
st.title(sh.PAGE_TITLES[PAGE])

# dataset
fname = rw.sources["data"][PAGE]
metadata = fp.ParquetFile(fname)
columns_to_read = ["Record", cb.COL_INST_NAME]
columns_with_text = [
    column for column in metadata.columns if column not in columns_to_read
]
dset = rw.read_parquet(fname, columns_to_read)

# logs
logs = rw.get_logs(PAGE)

cols = st.columns(2)
with cols[0]:
    vis.display_metrics(dset)
with cols[1]:
    st.link_button(sh.BROWSE_STATEMENTS_HEADER, rw.INSTITUTION_ENV_PATH)

with st.container(border=True):
    institutions = st.multiselect(
        sh.SELECT_INSTITUTION_PROMPT,
        dset[cb.COL_INST_NAME].unique(),
        placeholder=sh.SELECT_INSTITUTION_PLACEHOLDER,
    )
    section = st.selectbox(sh.SELECT_SECTION_PROMPT, metadata.columns[1:-1])

    keyword = st.text_input(sh.SEARCH_TERM_PROMPT, key="inst_search_term")

    if section and keyword:
        if not institutions:
            query_result = duckdb.query(
                f"""
                SELECT * FROM read_parquet('{fname}')
                WHERE "{section}" ILIKE '%{keyword}%'
            """
            )
        else:
            institutions = str(tuple(institutions))
            query_result = duckdb.query(
                f"""
                SELECT * FROM read_parquet('{fname}')
                WHERE "{cb.COL_INST_NAME}" IN {institutions} AND "{section}" ILIKE '%{keyword}%'
            """
            )
        qdset = query_result.to_df()
        if qdset.shape[0] == 0:
            st.error(sh.NO_SELECTED_RECORDS_WARNING)
        else:
            st.metric(sh.HITS_LABEL, qdset.shape[0])
            st.dataframe(qdset[[cb.COL_INST_NAME, section]])

with st.expander(sh.DESCRIBE_HEADER):
    vis.display_fields(dset)
    for column_name in columns_with_text:
        st.markdown(f"**{column_name}** - *{sh.EXTRACTED_TEXT_DESCRIPTION}*")
    vis.display_logs(logs)
