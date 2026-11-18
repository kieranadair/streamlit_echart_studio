"""Render just the selected part of the option; keep edits in the document."""

import streamlit as st

from .schema import catalog, matches


def value_input(spec, value, key):
    label = "Value" + (f" ({spec.unit})" if spec.unit not in ("", "color") else "")
    if spec.unit == "number":
        return st.number_input("Value", value=value, key=key)
    if spec.unit == "statistic":
        statistic = st.selectbox(
            "Statistic",
            spec.choices,
            index=spec.choices.index(value[0]["type"]),
            key=key,
        )
        return [{"type": statistic}]
    if spec.choices:
        return st.selectbox(
            label,
            spec.choices,
            index=spec.choices.index(value),
            key=key,
            format_func=lambda v: str(v).lower() if isinstance(v, bool) else str(v),
        )
    if spec.bounds:
        is_percent = spec.unit == "%"
        current = int(value[:-1]) if is_percent else value
        result = st.slider(label, *spec.bounds, value=current, key=key)
        return f"{result}%" if is_percent else result
    if isinstance(value, bool):
        return st.toggle("Value", value=value, key=key)
    if spec.unit == "color":
        return st.color_picker(label, value, key=key)
    return st.text_input(label, value, key=key)


def series_picker(doc, sample, key):
    measures = st.multiselect(
        "series · measures",
        sample.measures,
        default=doc.measures,
        key=key + ":measures",
        help="Each measure creates a separate series with its own styling.",
    )
    doc.measures = measures
    if not measures:
        st.info("Choose a measure to start a series.")
        return None
    col, kind_col = st.columns(2)
    measure = col.selectbox("Edit series", measures, key=key + ":active")
    series = doc.series[measure]
    kinds = ["bar", "line"]
    series.kind = kind_col.radio(
        "series.type",
        kinds,
        index=kinds.index(series.kind),
        horizontal=True,
        key=f"{key}:{measure}:type",
    )
    return measure


def property_editor(doc, sample, measure, key):
    series = doc.series[measure]
    sections = catalog(series.kind, sample.time_axis)
    query = st.text_input(
        "Find a property",
        placeholder="barGap, rotate tick labels, hover…",
        key="property_search",
        icon=":material/search:",
    )
    if query.strip():
        found = matches(sections, query)
        if not found:
            st.caption("No matching property for this series type. Try a shorter term.")
            return
        section, path = st.selectbox(
            "Matching properties",
            found,
            format_func=lambda pair: ".".join(pair),
            key=f"{key}:results:{series.kind}",
        )
    else:
        branch_col, property_col = st.columns([0.8, 1.4])
        section = branch_col.selectbox(
            "Option branch", list(sections), key=key + ":branch"
        )
        names = list(sections[section])
        initial = (
            names.index("barWidth")
            if section == "series" and series.kind == "bar"
            else 0
        )
        path = property_col.selectbox(
            "Property", names, index=initial, key=f"{key}:{section}:{series.kind}:path"
        )
    spec = sections[section][path]
    if section not in ("series", "xAxis", "yAxis"):
        include = st.toggle(
            f"Include {section}",
            section in doc.enabled,
            key=f"{key}:{section}:enabled",
            help="Switch this branch off to omit it. Its settings are remembered.",
        )
        if include:
            doc.enabled.add(section)
        else:
            doc.enabled.discard(section)
    branch_on = section == "series" or section in doc.enabled
    values = series.settings(path) if section == "series" else doc.components[section]
    full_path = (
        f"series[{doc.measures.index(measure)}].{path}"
        if section == "series"
        else (path if section == "animation" else f"{section}.{path}")
    )
    widget = f"{key}:{section}:{path}"
    if section == "series":
        widget += f":{measure}:{series.kind}"
    with st.container(border=True):
        st.markdown(f"**`{full_path}`**")
        st.write(spec.hint)
        if not branch_on:
            st.caption(f"Enable {section} to edit this property.")
        else:
            included = st.toggle(
                "Include property", path in values, key=widget + ":included"
            )
            if included:
                values[path] = value_input(
                    spec, values.get(path, spec.seed), widget + ":value"
                )
            else:
                values.pop(path, None)
        doc_path = f"series-{series.kind}.{path}" if section == "series" else full_path
        st.caption(
            f"[ECharts reference ↗](https://echarts.apache.org/en/option.html#{doc_path})"
        )
