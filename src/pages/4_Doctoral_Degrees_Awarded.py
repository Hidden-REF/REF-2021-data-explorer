import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.chart_container import chart_container
import plotly.figure_factory as ff

import codebook as cb
import read_write as rw
import process as proc
import visualisations as vis
import shared as sh


page_title = "Doctoral Degrees Awarded"
st.title(page_title)

with st.spinner(sh.PROC_TEXT):
    (dset, _) = rw.get_data(rw.DATA_PPROC_DEGREES)

vis.display_record_counts_table(dset)

# distribution charts
# -------------------
st.subheader(sh.CHARTS_HEADER)
dcolumns = [cb.COL_PANEL_NAME,
            cb.COL_UOA_NAME]
dtabs = st.tabs(dcolumns)

for i, column in enumerate(dcolumns):
    with dtabs[i]:
        dset_stats = proc.calculate_counts(dset,
                                           column,
                                           sort=False)
        with chart_container(dset_stats, export_formats=sh.DATA_EXPORT_FORMATS):
            vis.draw_counts_percent_chart(dset_stats,
                                          column)

# histograms
# ----------
st.subheader(cb.COL_DEGREES_TOTAL)
bin_size = st.slider("Select the bin size",
                     min_value=1,
                     max_value=50,
                     value=10,
                     step=1)

fig = ff.create_distplot([dset[cb.COL_DEGREES_TOTAL]],
                         [cb.COL_DEGREES_TOTAL],
                         histnorm="probability",
                         show_rug=True,
                         show_curve=False,
                         bin_size=bin_size)
fig.update_layout(showlegend=False,
                  margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

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
