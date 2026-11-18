import json

import streamlit as st

from echarts_studio.data import SAMPLES
from echarts_studio.editor import property_editor, series_picker
from echarts_studio.options import Document

st.set_page_config(
    page_title="ECharts Studio", page_icon=":material/bar_chart:", layout="wide"
)
st.title("ECharts Studio")
st.caption("Explore the Apache ECharts option, one property at a time.")

with st.container(border=True):
    selector, summary = st.columns([1, 2], vertical_alignment="bottom")
    name = selector.selectbox("Dataset", list(SAMPLES), key="dataset", width=320)
    sample = SAMPLES[name]
    summary.caption(f"{sample.lesson} Showing 3 of {len(sample.rows)} sample rows.")
    st.dataframe(
        sample.records()[:3],
        hide_index=True,
        row_height=25,
        alt=f"First three records from {name}",
    )

if "documents" not in st.session_state:
    st.session_state.documents = {}
if name not in st.session_state.documents:
    st.session_state.documents[name] = Document.for_sample(sample)
doc = st.session_state.documents[name]

editor, preview = st.columns([0.88, 1.35], gap="large")
with editor:
    st.subheader("Option explorer")
    with st.expander("Configure series", icon=":material/tune:"):
        measure = series_picker(doc, sample, name)
    if measure:
        property_editor(doc, sample, measure, name)

with preview:
    st.subheader("Live chart")
    option = doc.build(sample)
    with st.container(border=True):
        if doc.measures:
            st.echarts_chart(
                option,
                height=340,
                theme=None,
                alt=f"{', '.join(doc.measures)} by {sample.dimension} for {name}",
            )
        else:
            st.info("Add a series in the option explorer to draw the chart.")
    prompts = {
        "Monthly retail": "Open Configure series and add Target. Select Target and switch its type to line to compare it with the revenue bars.",
        "Regional channels": "Add Online. Compare barGap and barCategoryGap on the last bar series, then give both series the same stack name.",
        "Weather log": "Switch High to line. Add connectNulls, then toggle its value to inspect the gap in late April.",
    }
    st.caption(f"**Try this** · {prompts[name]}")
    contract = st.expander(
        "View ECharts option", icon=":material/data_object:", on_change="rerun"
    )
    if contract.open:
        with contract:
            st.code(
                json.dumps(option, indent=2, allow_nan=False),
                language="json",
                height=360,
            )
