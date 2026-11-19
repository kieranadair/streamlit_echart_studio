import streamlit as st

from echarts_studio.controls import preview_size
from echarts_studio.data import EXAMPLE_DATASETS, SAMPLES
from echarts_studio.editor import data_bindings, property_editor
from echarts_studio.options import Document, option_code

st.set_page_config(
    page_title="ECharts Studio", page_icon=":material/bar_chart:", layout="wide"
)
st.title("ECharts Studio")


def focus_example():
    st.session_state.property_search = ""
    st.session_state.option_branches = {
        "Bubble plot": "visualMap",
        "Heatmap": "visualMap",
        "Rank the regions": "dataset",
        "Linked panels": "grid",
        "Responsive layout": "media",
    }.get(st.session_state.example, "series")


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
    tables = st.container()

editor, preview = st.columns([1.2, 1], gap="medium")
with editor:
    st.subheader("Option explorer")
    property_editor(doc, df, key)
with (
    preview,
    st.container(
        horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"
    ),
):
    st.subheader("Live chart")
    preview_size(doc, key)
result = doc.compile(df)
option = result.option
with editor:
    contract = st.expander(
        "View ECharts option", icon=":material/data_object:", on_change="rerun"
    )
    if contract.open:
        with contract:
            st.caption("`df` is the selected DataFrame shown above.")
            if result.trends:
                st.caption(
                    "The trend_df variables refer to the calculated tables under the data bindings."
                )
            st.code(option_code(option), language="python", height=320)

if doc.transform.filter_field or doc.transform.sort_field or result.trends:
    with tables.expander(
        f"Inspect plotted data · {len(result.plotted)} rows", on_change="rerun"
    ) as detail:
        if detail.open:
            if doc.transform.filter_field or doc.transform.sort_field:
                st.caption(f"Source · df · {len(df)} rows")
                st.dataframe(
                    df,
                    hide_index=True,
                    height=160,
                    alt="Original observations before transforms",
                )
                st.caption("Plotted rows · dataset[1] after ECharts filter and sort")
                st.dataframe(
                    result.plotted,
                    hide_index=True,
                    height=160,
                    alt="Observations after the dataset transforms",
                )
            for i, (explanation, derived) in enumerate(result.trends, 1):
                title = derived.columns[-1]
                st.caption(f"`trend_df_{i}` · {title}")
                st.caption(explanation)
                st.dataframe(derived, hide_index=True, height=160, alt=title)

with preview:
    if doc.measures:
        with st.container(border=True):
            descriptions = []
            for measure in doc.measures:
                series = doc.series[measure]
                x, y = doc.bindings(measure)
                description = f"{x} on X, {y} on Y"
                if doc.category_y:
                    description += f", colour by {measure}"
                elif series.kind == "scatter" and series.mapping.dimension:
                    description += f", point size by {series.mapping.dimension}"
                descriptions.append(description)
            if any(doc.series[m].kind == "scatter" for m in doc.measures):
                st.caption(" · ".join(descriptions))
            st.echarts_chart(
                option,
                height=doc.preview_height,
                width=doc.preview_width or "stretch",
                theme=None,
                key="live_chart",
                alt=None
                if "aria" in doc.enabled
                else f"{name} · {', '.join(descriptions)}",
            )
        if len(doc.x_fields()) > 1 and not (doc.panels and "grid" in doc.enabled):
            st.caption(
                " · ".join(
                    f"`{doc.dimension_axis}[{i}]` {column}"
                    for i, column in enumerate(doc.x_fields())
                )
            )
    else:
        st.info("Select a measure above to draw the chart.")
    if result.plotted.empty:
        st.info(
            "The filter matched zero rows. Change the filter value to bring observations back."
        )
    for message in result.messages:
        st.info(message)
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
        "Rank the regions": "Change sort order or set a filter in dataset. Compare the source and plotted rows.",
        "Benchmarks and bands": "Edit a threshold or move a band endpoint under series. Compare the fixed benchmark with the calculated mean.",
        "Linear fit": "Inspect the fitted endpoints under the data bindings, then filter the observations to fit the line again.",
        "Moving average": "Open Calculated trend in series and change the trailing window. Inspect the first row with a complete window.",
        "Linked panels": "Hover across the panels, then turn off axisPointer.link in grid to compare the pointers.",
        "Responsive layout": "Use Preview size to cross the media breakpoint and watch the legend move.",
    }
    st.caption(f"**Try this** · {lessons[example]}")
