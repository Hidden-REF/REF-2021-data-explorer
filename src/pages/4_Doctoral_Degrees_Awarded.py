import pandas as pd
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

dset_to_print = pd.DataFrame.from_dict(
    {
        "Doctoral degrees records": dset.shape[0],
        "Institutions": dset[cb.COL_INST_NAME].nunique()
    },
    orient="index"
    )
dset_to_print.columns = ["count"]
pd.set_option("display.max_colwidth", None)
st.dataframe(dset_to_print)

st.subheader(sh.CHARTS_HEADER)
st.markdown("Select from the charts below to view the "
            "distributions for the number of doctoral degrees records by ...")


columns = [cb.COL_PANEL_NAME,
           cb.COL_UOA_NAME]
tabs = st.tabs(columns)

for i, column in enumerate(columns):
    with tabs[i]:
        dset_stats = proc.calculate_counts(dset,
                                           column,
                                           sort=False)
        with chart_container(dset_stats):
            vis.draw_counts_percent_chart(dset_stats,
                                          column)

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

st.subheader(sh.EXPLORE_HEADER)
dset_explore = dataframe_explorer(dset)
st.dataframe(dset_explore, use_container_width=False)
