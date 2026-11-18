import streamlit as st

from echarts_studio.data import SAMPLES
from echarts_studio.editor import data_bindings, property_editor
from echarts_studio.options import Document, option_code

st.set_page_config(
    page_title="ECharts Studio", page_icon=":material/bar_chart:", layout="wide"
)
st.title("ECharts Studio")

with st.container(border=True):
    selector, summary = st.columns([1, 2], vertical_alignment="bottom")
    name = selector.selectbox("Dataset", list(SAMPLES), key="dataset", width=320)
    sample = SAMPLES[name]
    df = sample.dataframe()
    summary.caption(f"{sample.lesson} Showing 3 of {len(df)} rows.")
    st.dataframe(
        df.head(3),
        hide_index=True,
        row_height=25,
        alt=f"First three records from {name}",
    )
    if "documents" not in st.session_state:
        st.session_state.documents = {}
    if name not in st.session_state.documents:
        st.session_state.documents[name] = Document.for_sample(sample)
    doc = st.session_state.documents[name]
    data_bindings(doc, df, sample, name)

editor, preview = st.columns([1.2, 1], gap="medium")
with editor:
    st.subheader("Option explorer")
    property_editor(doc, df, name)
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
            descriptions = [f"{m} by {doc.x_for(m)}" for m in doc.measures]
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
    st.caption(f"**Try this** · {prompts[name]}")
