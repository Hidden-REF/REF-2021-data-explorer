# pylint: disable=C0103
# pylint: disable=R0801
# pylint: disable=E0401
# pylint: disable=R1729
""" Results page"""
import numpy as np
import altair as alt
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

import REF2021_explorer.codebook as cb
import REF2021_explorer.visualisations as vis
import REF2021_explorer.shared_content as sh

PAGE = "results"

(dset, logs) = sh.prepare_page(PAGE)

vis.display_metrics(dset)

dset_explore = dataframe_explorer(dset)
if dset_explore.shape[0] == 0:
    st.warning(sh.NO_SELECTED_RECORDS_WARNING)
else:
    data_prefix = ""
    labels = [
        f"{sh.SELECTED_LABEL} {sh.RECORDS_LABEL.lower()}",
        f"{sh.SELECTED_LABEL} {sh.INSTITUTIONS_LABEL.lower()}",
    ]
    if dset_explore.shape[0] < dset.shape[0]:
        data_prefix = " selected"

    tabs = st.tabs(sh.PROFILE_HEADERS.values())
    column_prefixes = [f"{key} profile - " for key, _ in sh.PROFILE_HEADERS.items()]
    for key, value in sh.PROFILE_HEADERS.items():
        with tabs[list(sh.PROFILE_HEADERS.values()).index(value)]:
            columns_prefix = f"{key} profile - "
            exclude_prefixes = column_prefixes.copy()
            exclude_prefixes.remove(columns_prefix)
            columns = [
                col
                for col in dset.columns
                if col != cb.COL_MAIN_PANEL_NAME
                and (
                    col.startswith(columns_prefix)
                    or not any(
                        [col.startswith(exclude) for exclude in exclude_prefixes]
                    )
                )
            ]
            if key == "Outputs":
                columns = [
                    col
                    for col in columns
                    if not col.startswith("Impact")
                    and not col.startswith("Total number")
                ]
            elif key == "Impact":
                columns = [
                    col
                    for col in columns
                    if not col.startswith("Output")
                    and not col.startswith("Total number")
                ]
            elif key == "Environment":
                columns = [
                    col
                    for col in columns
                    if not col.startswith("Output")
                    and not col.startswith("Impact")
                    and not col.startswith("Total number")
                ]

            dset_to_display = dset_explore[columns].copy()
            vis.display_metrics(dset_to_display, labels=labels)
            dset_to_display.columns = [
                col.replace(columns_prefix, "")
                .replace(" stars", "*")
                .replace(" star", "*")
                .replace("Output submissions - ", "Outputs - ")
                .replace("Output submissions", "Outputs")
                .replace(" (added)", "")
                for col in dset_to_display.columns
            ]
            # calculate GPA
            dset_to_display["GPA"] = np.round(
                (
                    (
                        dset_to_display["4*"] * 4
                        + dset_to_display["3*"] * 3
                        + dset_to_display["2*"] * 2
                        + dset_to_display["1*"]
                    )
                    / 100
                ),
                decimals=2,
            )
            # insert the GPA column after Unclassified
            dset_to_display.insert(
                dset_to_display.columns.get_loc("Unclassified") + 1,
                "GPA",
                dset_to_display.pop("GPA"),
            )

            st.dataframe(dset_to_display, hide_index=True, use_container_width=False)

            if key in ["Outputs", "Impact"]:
                if key == "Outputs":
                    columns_x = ["Outputs", "% of eligible staff submitted", "GPA"]
                elif key == "Impact":
                    columns_x = [
                        "Impact case study submissions",
                        "% of eligible staff submitted",
                        "GPA",
                    ]
                column_x = st.selectbox(
                    "Select the variable for the x axis",
                    columns_x,
                    key=f"{key}_x",
                )

                columns_y = ["4*", "3*", "2*", "1*"]
                if column_x != "GPA":
                    columns_y.append("GPA")
                column_y = st.selectbox(
                    "Select the variable for the y axis",
                    columns_y,
                    key=f"{key}_y",
                )

                if column_x and column_y:
                    correlation_coefficient = dset_to_display[column_x].corr(
                        dset_to_display[column_y]
                    )
                    scatter = (
                        alt.Chart(dset_to_display)
                        .mark_circle()
                        .encode(x=column_x, y=column_y)
                    )
                    line = scatter.transform_regression(column_x, column_y).mark_line(
                        color="red"
                    )

                    chart = (scatter + line).properties(
                        title=f"Correlation coefficient: {correlation_coefficient:.2f}"
                    )

                    st.altair_chart(chart, use_container_width=True)

# with st.expander(sh.VISUALISE_HEADER):
#     vis.display_data_explorer(dset)

# with st.expander(sh.DESCRIBE_HEADER):
#     vis.display_data_description(dset, description=sh.GROUPS_DESCRIPTION)

# with st.expander(sh.LOGS_HEADER):
#     vis.display_logs(logs)
