import streamlit as st

from echarts_studio.data import EXAMPLE_DATASETS, SAMPLES
from echarts_studio.editor import data_bindings, property_editor
from echarts_studio.options import Document, option_code

st.set_page_config(
    page_title="ECharts Studio", page_icon=":material/bar_chart:", layout="wide"
)
st.title("ECharts Studio")


def focus_example():
    st.session_state.property_search = ""
    st.session_state.option_branches = (
        "visualMap"
        if st.session_state.example in ("Bubble plot", "Heatmap")
        else "series"
    )


with st.container(border=True):
    starter, selector, summary = st.columns([1, 1, 2], vertical_alignment="bottom")
    example = starter.selectbox(
        "Starting example",
        list(EXAMPLE_DATASETS),
        key="example",
        on_change=focus_example,
    )
    dataset_key = "dataset" if example == "Bar chart" else f"{example}:dataset"
    name = selector.selectbox(
        "Dataset",
        list(SAMPLES),
        index=list(SAMPLES).index(EXAMPLE_DATASETS[example]),
        key=dataset_key,
        persist_state="session",
    )
    sample = SAMPLES[name]
    heatmap = example == "Heatmap"
    df = sample.dataframe(heatmap=heatmap)
    layout_hint = " One row per cell." if heatmap else ""
    summary.caption(f"{sample.lesson}{layout_hint} Showing 3 of {len(df)} rows.")
    st.dataframe(
        df.head(3),
        hide_index=True,
        row_height=25,
        alt=f"First three records from {name}",
    )
    if "documents" not in st.session_state:
        st.session_state.documents = {}
    key = name if example == "Bar chart" else f"{name}:{example}"
    if key not in st.session_state.documents:
        st.session_state.documents[key] = Document.for_sample(sample, example, df)
    doc = st.session_state.documents[key]
    data_bindings(doc, df, sample, key)

editor, preview = st.columns([1.2, 1], gap="medium")
with editor:
    st.subheader("Option explorer")
    property_editor(doc, df, key)
    option = doc.build(df)
    contract = st.expander(
        "View ECharts option", icon=":material/data_object:", on_change="rerun"
    )
    if contract.open:
        with contract:
            st.caption("`df` is the selected DataFrame shown above.")
            st.code(option_code(option), language="python", height=320)

with preview:
    st.subheader("Live chart")
    if doc.measures:
        with st.container(border=True):
            descriptions = []
            for measure in doc.measures:
                series = doc.series[measure]
                description = (
                    f"{doc.x_for(measure)} on X, {doc.category_y or measure} on Y"
                )
                if doc.category_y:
                    description += f", colour by {measure}"
                elif series.kind == "scatter" and series.mapping.dimension:
                    description += f", point size by {series.mapping.dimension}"
                descriptions.append(description)
            if any(series["type"] == "scatter" for series in option["series"]):
                st.caption(" · ".join(descriptions))
            st.echarts_chart(
                option,
                height=560,
                theme=None,
                key="live_chart",
                alt=f"{name}: {', '.join(descriptions)}",
            )
        if len(doc.x_fields()) > 1:
            st.caption(
                " · ".join(
                    f"`xAxis[{i}]` {column}" for i, column in enumerate(doc.x_fields())
                )
            )
    else:
        st.info("Select a Y field above to draw the chart.")
    prompts = {
        "Monthly retail": "Add Target to the Y fields, then change its series.type to line.",
        "Regional channels": "Add Online. Compare barGap and barCategoryGap on the last bar series, then give both series the same stack name.",
        "Weather log": "Add Low, then set its encode.x to Day. High will keep the shared Date axis.",
    }
    lessons = {
        "Bar chart": prompts[name],
        "Stacked bars": f"Select {sample.measures[1]} in the series tab and reset its stack name to move it out of the stack.",
        "Area chart": "Reset areaStyle.opacity and watch the fill disappear.",
        "Scatter plot": "Change symbol or symbolSize. Then choose a numeric field in visualMap to vary the point sizes.",
        "Bubble plot": "Change inRange.symbolSize in visualMap, then switch the size field to fixed to compare the points.",
        "Heatmap": "Change visualMap.min or max to adjust the colour contrast. The source values stay the same.",
    }
    st.caption(f"**Try this** · {lessons[example]}")
