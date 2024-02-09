""" Institution environment statements page """
import streamlit as st
import fastparquet as fp

import codebook as cb
import read_write as rw
import visualisations as vis
import shared_content as sh

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

vis.display_metrics(dset)

st.link_button(
    sh.BROWSE_STATEMENTS_HEADER,
    rw.INSTITUTION_ENV_PATH
)

with st.expander(sh.DESCRIBE_HEADER):
    vis.display_fields(dset)
    for column_name in columns_with_text:
        st.markdown(f"**{column_name}** - *{sh.EXTRACTED_TEXT_DESCRIPTION}*")
    vis.display_logs(logs)
