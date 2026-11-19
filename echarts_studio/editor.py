"""Direct-edit controls for the active option branch."""

from collections import defaultdict
from collections.abc import Callable
from typing import Literal, TypedDict

import streamlit as st

from . import controls
from .controls import sync as _sync
from .schema import OPTIONAL_BRANCHES, VISUAL_MAP_STYLE, catalog, matches


def _change_heatmap_axis(doc, axis, key):
    # Swapping Channel and Region must keep each cell uniquely addressable.
    other = "category_y" if axis == "shared_x" else "shared_x"
    column = st.session_state[key]
    if column == getattr(doc, other):
        setattr(doc, other, getattr(doc, axis))
    setattr(doc, axis, column)


def data_bindings(doc, frame, sample, key):
    if doc.category_y is not None:
        categories = frame.select_dtypes(exclude="number").columns.tolist()
        x_col, y_col, value_col = st.columns(3)
        for container, axis, label in (
            (x_col, "shared_x", "X category · encode.x"),
            (y_col, "category_y", "Y category · encode.y"),
        ):
            widget = f"{key}:{axis}"
            _sync(widget, getattr(doc, axis))
            container.selectbox(
                label,
                categories,
                key=widget,
                on_change=_change_heatmap_axis,
                args=(doc, axis, widget),
            )
        numeric = list(doc.series)
        value = value_col.selectbox(
            "Cell value · encode.value",
            numeric,
            index=numeric.index(doc.measures[0]),
            key=key + ":cell-value",
            help="visualMap maps this column to the cell colour.",
        )
        doc.measures = [value]
        return
    doc.horizontal = st.toggle(
        "Swap X and Y",
        doc.horizontal,
        key=key + ":horizontal",
        help="Put measures on X and their shared dimension on Y. Bar series become horizontal.",
    )
    left, right = st.columns(2)
    x_col, y_col = (right, left) if doc.horizontal else (left, right)
    columns = frame.columns.tolist()
    doc.shared_x = x_col.selectbox(
        "Shared Y field · encode.y" if doc.horizontal else "Shared X field · encode.x",
        columns,
        index=columns.index(doc.shared_x),
        key=key + ":shared-x",
        help="Each series uses this dimension unless you override its binding in the series tab.",
    )
    doc.measures = y_col.multiselect(
        "X fields · encode.x" if doc.horizontal else "Y fields · encode.y",
        sample.measures,
        default=doc.measures,
        key=key + ":measures",
        help="Each selected measure creates one series.",
    )


def _write_attribute(obj, attribute, key):
    setattr(obj, attribute, st.session_state[key])


def _series_controls(doc, measure, frame, key):
    col1, col2, col3 = st.columns([1, 0.8, 1.25])
    col1.selectbox(
        "Edit series",
        doc.measures,
        index=doc.measures.index(measure),
        key=key + ":active",
        persist_state="page",
    )
    series = doc.series[measure]
    type_key = f"{key}:{measure}:type"
    kinds = ["bar", "line", "scatter"]
    col2.selectbox(
        "series.type",
        kinds,
        index=kinds.index(series.kind),
        key=type_key,
        help="These series can share an X/Y chart. Choose the Heatmap starting example for a two-category matrix.",
        on_change=_write_attribute,
        args=(series, "kind", type_key),
    )
    x_key = f"{key}:{measure}:encode.x"
    fields = [None, *frame.columns]
    col3.selectbox(
        "encode.y" if doc.horizontal else "encode.x",
        fields,
        index=fields.index(series.x_override),
        key=x_key,
        format_func=lambda column: (
            f"Shared · {doc.shared_x}" if column is None else column
        ),
        on_change=_write_attribute,
        args=(series, "x_override", x_key),
        help="Use a separate dimension for this series. Each distinct dimension gets its own axis.",
    )

    if series.kind == "scatter":
        if series.mapping.dimension:
            st.caption(
                f"Point size is mapped to **{series.mapping.dimension}** in the visualMap tab."
            )
        else:
            st.caption(
                "Choose a dimension in the visualMap tab to size points by a field."
            )


def _literal(value):
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _widget_value(spec, value):
    if spec.kind == "feature":
        return isinstance(value, dict)
    if spec.kind == "percent":
        return None if value is None else int(value.removesuffix("%"))
    if spec.kind == "statistic":
        return value[0]["type"] if value else None
    if spec.kind == "length" and isinstance(value, (int, float)):
        return f"{value:g}px"
    if value is None and spec.kind in ("color", "text"):
        return ""
    return value


def _option_value(spec, value):
    if spec.kind == "feature":
        return {} if value else None
    if value is None or value == "":
        return None
    if spec.kind == "percent":
        return f"{value}%"
    if spec.kind == "statistic":
        return [{"type": value}]
    if spec.kind == "length":
        units = value.strip()
        magnitude = float(units.removesuffix("%").removesuffix("px"))
        if units.endswith("%"):
            return f"{magnitude:g}%"
        return int(magnitude) if magnitude.is_integer() else magnitude
    if spec.kind == "color":
        value = value.strip().lower()
        if value.startswith("#") and len(value) == 4:
            return "#" + "".join(c * 2 for c in value[1:])
    return value


def _commit(values, path, spec, key):
    value = _option_value(spec, st.session_state[key])
    if value is None or value == spec.default:
        values.pop(path, None)
    else:
        values[path] = value


def _pick_color(values, path, spec, key, initial):
    # An automatic or translucent colour has no corresponding hex swatch.
    # Mounting the picker can echo its starting colour back from the browser.
    if st.session_state[key].lower() != initial.lower():
        _commit(values, path, spec, key)


class WidgetArgs(TypedDict):
    key: str
    label_visibility: Literal["collapsed"]
    disabled: bool
    on_change: Callable
    args: tuple


def _input(spec, values, path, label, key, disabled):
    value = _widget_value(spec, values.get(path, spec.default))
    _sync(key, value)
    kwargs: WidgetArgs = {
        "key": key,
        "label_visibility": "collapsed",
        "disabled": disabled,
        "on_change": _commit,
        "args": (values, path, spec, key),
    }
    if spec.kind in ("choice", "statistic"):
        st.selectbox(
            label,
            spec.choices,
            index=None,
            placeholder=spec.placeholder,
            format_func=_literal,
            **kwargs,
        )
    elif spec.kind in ("bool", "feature"):
        st.toggle(label, **kwargs)
    elif spec.kind in ("number", "percent"):
        lo, hi = spec.bounds
        step = 1 if isinstance(lo, int) else (0.05 if hi == 1.0 else 0.1)
        st.number_input(
            label,
            min_value=lo,
            max_value=hi,
            step=step,
            value=None,
            placeholder=spec.placeholder or "Default",
            **kwargs,
        )
    elif spec.kind == "length":
        st.text_input(
            label,
            validate=(
                r"^\d+(?:\.\d+)?(?:px|%)?$",
                "Enter a length such as 65px or 15%.",
            ),
            **kwargs,
        )
    elif spec.kind == "color":
        # The text control can show inherited/transparent colours; the swatch
        # lets the learner choose an opaque colour visually.
        st.text_input(
            label,
            placeholder=spec.placeholder,
            validate=(
                r"^(?:#[a-fA-F0-9]{3}|#[a-fA-F0-9]{6}|rgba?\([\d\s.,%]+\))$",
                "Enter a hex, rgb(), or rgba() colour.",
            ),
            **kwargs,
        )
        picker = key + ":swatch"
        swatch = value if value.startswith("#") else "#425bbd"
        _sync(picker, swatch)
        st.color_picker(
            f"Choose {label} colour",
            key=picker,
            label_visibility="collapsed",
            disabled=disabled,
            on_change=_pick_color,
            args=(values, path, spec, picker, swatch),
        )
    else:
        st.text_input(label, placeholder=spec.placeholder, **kwargs)


def _row(path, spec, values, prefix, doc_branch, key, enabled):
    doc_path = f"{doc_branch}.{path}" if doc_branch else path
    full_path = f"{prefix}.{path}" if prefix else path
    edited = path in values
    status = ":blue[● Configured]" if edited and enabled else ":gray[○ Default]"
    if edited and not enabled:
        status = ":gray[● Saved · branch off]"
    left, right = st.columns([1.4, 1], vertical_alignment="center", gap="small")
    with left.container(gap=None):
        unit = f" ({spec.unit})" if spec.unit else ""
        st.markdown(
            f"[`{full_path}`](https://echarts.apache.org/en/option.html#{doc_path}){unit} {status}"
        )
        st.caption(spec.hint)
    with right.container(horizontal=True, vertical_alignment="center", gap="xsmall"):
        _input(spec, values, path, full_path, key, not enabled)
        if edited:
            default = (
                spec.placeholder if spec.default is None else _literal(spec.default)
            )
            st.button(
                ":material/restart_alt:",
                help=f"Reset {full_path} to {default or 'empty'}",
                type="tertiary",
                key=key + ":reset",
                disabled=not enabled,
                on_click=values.pop,
                args=(path, None),
            )


def _focused(widget_key, options):
    current = st.session_state.get(widget_key)
    return current if current in options else next(iter(options), None)


def _set_limit(mapping, column, observed, index, key):
    limits = list(mapping.domains.get(column, observed))
    value = st.session_state[key]
    limits[index] = observed[index] if value is None else value
    if limits[0] >= limits[1]:
        st.toast("visualMap.min must be smaller than visualMap.max.")
    elif tuple(limits) == observed:
        mapping.domains.pop(column, None)
    else:
        mapping.domains[column] = tuple(limits)


def _visual_map_controls(doc, frame, targets, focused, key, paths):
    target = targets[0]
    if len(targets) > 1:
        target = st.selectbox(
            "Target series · seriesIndex",
            targets,
            index=targets.index(focused) if focused in targets else 0,
            format_func=lambda m: f"{m} · series[{doc.measures.index(m)}]",
            key=key + ":map-target",
        )
    else:
        st.caption(
            f"`visualMap.seriesIndex = {doc.measures.index(target)}` targets **{target}**."
        )
    mapping = doc.series[target].mapping
    scope = f"{key}:visualMap:{target}"
    heatmap = doc.category_y is not None
    if heatmap:
        column = target
        if paths & {"type", "pieces", "min", "max", "inRange.color", "calculable"}:
            mapping.kind = controls.select(
                st,
                "visualMap.type",
                ["continuous", "piecewise"],
                mapping.kind,
                scope + ":type",
            )
    else:
        fixed = "Fixed series.symbolSize"
        options = [fixed, *frame.select_dtypes("number").columns]
        selected = st.selectbox(
            "Size field · visualMap.dimension",
            options,
            index=options.index(mapping.dimension or fixed),
            key=scope + ":dimension",
            help="Choose a numeric field to enable bubble sizing. Return to fixed size to remove this mapping.",
        )
        mapping.dimension = None if selected == fixed else selected
        if mapping.dimension is None:
            return
        column = mapping.dimension

    if "dimension" in paths:
        role = "cell colour" if heatmap else "point size"
        st.caption(
            f"`visualMap.dimension = {frame.columns.get_loc(column)}` maps **{column}** to {role}. DataFrame column indices start at zero."
        )
    piecewise = heatmap and mapping.kind == "piecewise"
    if piecewise and paths & {"type", "pieces"}:
        controls.piece_controls(mapping, frame, column, scope)
    elif piecewise and paths & {"min", "max", "inRange.color", "calculable"}:
        st.caption(
            "Choose continuous to edit the scale limits, gradient or draggable handles."
        )
    elif not piecewise and "pieces" in paths and "type" not in paths:
        st.caption("Choose piecewise to edit the colour bands.")
    if not piecewise and paths & {"min", "max"}:
        observed = mapping.data_range(frame[column])
        limits = mapping.domains.get(column, observed)
        low, high = st.columns(2)
        for i, container, prop in ((0, low, "min"), (1, high, "max")):
            if prop in paths:
                widget = f"{scope}:{column}:{prop}"
                _sync(widget, limits[i])
                container.number_input(
                    f"visualMap.{prop}",
                    value=None,
                    step=0.1,
                    key=widget,
                    on_change=_set_limit,
                    args=(mapping, column, observed, i, widget),
                )
        st.caption(
            f"This example starts at **{observed[0]:g}–{observed[1]:g}** for {column}. "
            "ECharts defaults to 0–200 when both limits are omitted. "
            "[Scale limits](https://echarts.apache.org/en/option.html#visualMap-continuous.min)"
        )
        if column in mapping.domains:
            st.button(
                "Use data range",
                key=scope + ":reset-range",
                type="tertiary",
                on_click=mapping.domains.pop,
                args=(column, None),
            )
    if "inRange.symbolSize" in paths:
        mapping.sizes = st.slider(
            "visualMap.inRange.symbolSize (px)",
            1,
            80,
            mapping.sizes,
            key=scope + ":sizes",
            help="Marker sizes for the low and high ends of the scale. For circles these are diameters in pixels.",
        )
    if not piecewise and "inRange.color" in paths:
        low, high = st.columns(2)
        mapping.colours = (
            low.color_picker(
                "inRange.color[0] · low", mapping.colours[0], key=scope + ":low-colour"
            ).lower(),
            high.color_picker(
                "inRange.color[1] · high",
                mapping.colours[1],
                key=scope + ":high-colour",
            ).lower(),
        )

    active = [
        m for m in targets if heatmap or doc.series[m].mapping.dimension is not None
    ]
    prefix = f"visualMap[{active.index(target)}]" if len(active) > 1 else "visualMap"
    rows = {
        p: (spec, mapping.settings)
        for p, spec in VISUAL_MAP_STYLE.items()
        if p in paths and not (piecewise and p == "calculable")
    }
    _render_groups(
        rows,
        scope,
        prefix,
        "visualMap-piecewise" if piecewise else "visualMap-continuous",
        True,
    )


def _axis_controls(doc, frame, branch, dimension, key, paths):
    fields = doc.x_fields()
    per_dimension = branch == doc.dimension_axis
    if per_dimension and len(fields) > 1:
        st.selectbox(
            f"Edit {branch[0].upper()} axis",
            fields,
            index=fields.index(dimension),
            key=key + ":axis",
            persist_state="page",
        )
    scope = f"{key}:{branch}" + (f":{dimension}" if per_dimension else "")
    if doc.horizontal:
        scope += ":horizontal"
    values = doc.axis_settings(branch, dimension)
    inferred = doc.inferred_axis_type(branch, dimension, frame)
    kind = doc.axis_kind(branch, dimension, frame)
    prefix = (
        f"{branch}[{fields.index(dimension)}]"
        if per_dimension and len(fields) > 1
        else branch
    )
    if doc.panels and "grid" in doc.enabled and len(doc.measures) > 1:
        prefix = branch
        st.caption("These settings apply to the matching axes across panels.")
    if per_dimension:
        st.caption(f"`encode.{branch[0]} = {dimension!r}` · `{branch}.type = {kind!r}`")
    if "type" in paths:
        if doc.category_y:
            st.caption("Cartesian heatmaps use category bands on both axes.")
        else:
            kinds = list(dict.fromkeys([inferred, "category"]))
            widget = scope + ":type"
            _sync(widget, kind)

            def set_type():
                choice = st.session_state[widget]
                if choice == inferred:
                    values.pop("type", None)
                else:
                    values["type"] = choice

            st.selectbox(
                f"{prefix}.type",
                kinds,
                key=widget,
                on_change=set_type,
                help="The initial type follows the bound field. A numeric or date dimension can also be shown as categories.",
            )
    return scope, prefix, values


def _component_bindings(branch, doc, key, paths, enabled):
    if branch == "Chart" and "color" in paths:
        with st.expander("Series palette · color", expanded=len(paths) == 1):
            controls.palette_controls(doc.components["Chart"], key)
    elif branch == "grid" and paths & {"gridIndex", "axisPointer.link"}:
        controls.layout_controls(doc, key, enabled)
    elif branch == "media":
        controls.media_controls(doc, key, enabled)
    elif branch == "graphic" and "elements" in paths:
        col, inset = st.columns(2)
        doc.note_corner = controls.select(
            col,
            "Canvas corner",
            ["Top left", "Top right", "Bottom left", "Bottom right"],
            doc.note_corner,
            key + ":corner",
            disabled=not enabled,
        )
        doc.note_inset = inset.slider(
            "Edge inset (%)",
            0,
            25,
            doc.note_inset,
            key=key + ":inset",
            disabled=not enabled,
        )
    elif branch == "brush" and "toolbox" in paths:
        doc.brush_tools = st.multiselect(
            "Brush tools",
            ["rect", "polygon"],
            default=doc.brush_tools,
            key=key + ":tools",
            disabled=not enabled,
            help="Pick a shape in the chart toolbar, then drag across the marks. Clear removes the selection.",
        )
        if not any(doc.series[m].kind in ("bar", "scatter") for m in doc.measures):
            st.caption("Select a bar or scatter series to brush its marks.")


def property_editor(doc, frame, key):
    query = st.text_input(
        "Find a property",
        placeholder="Search by property or effect…",
        key="property_search",
        live=True,
        icon=":material/search:",
        label_visibility="collapsed",
    )
    measure = _focused(key + ":active", doc.measures)
    series = doc.series.get(measure)
    fields = doc.x_fields()
    dimension = _focused(key + ":axis", fields)
    targets = [m for m in doc.measures if doc.series[m].kind in ("scatter", "heatmap")]
    sections = catalog(
        series.kind if series else "bar",
        doc.axis_kind("xAxis", dimension, frame),
        len(fields) > 1,
        y_type=doc.axis_kind("yAxis", dimension, frame),
        mapping_kind=doc.series[targets[0]].kind if targets else None,
    )
    visible = matches(sections, query)
    branches = list(dict.fromkeys(section for section, _ in visible))
    if not branches:
        st.caption("No matching property. Try a shorter path or visual effect.")
        return

    tabs = st.tabs(branches, key="option_branches", on_change="rerun")
    for tab, branch in zip(tabs, branches, strict=True):
        if not tab.open:
            continue
        paths = [path for section, path in visible if section == branch]
        with tab, st.container(height=505, border=False):
            enabled = True
            scope = f"{key}:{branch}"
            prefix = reference = branch
            if branch == "visualMap":
                _visual_map_controls(doc, frame, targets, measure, key, set(paths))
                continue
            if branch == "dataset":
                controls.dataset_controls(doc, frame, scope)
                continue
            if branch == "series":
                if series is None:
                    st.info("Select a measure above to create a series.")
                    continue
                if doc.category_y is None:
                    _series_controls(doc, measure, frame, key)
                else:
                    st.caption(
                        "`series.type = 'heatmap'` · Each DataFrame row supplies one cell."
                    )
                scope = f"{key}:series:{measure}:{series.kind}"
                prefix = f"series[{doc.measures.index(measure)}]"
                reference = f"series-{series.kind}"
                controls.series_bindings(doc, measure, frame, scope, paths, bool(query))
                get_values = series.settings
            elif branch in ("xAxis", "yAxis"):
                scope, prefix, values = _axis_controls(
                    doc, frame, branch, dimension, key, paths
                )
            else:
                if branch in OPTIONAL_BRANCHES:
                    enabled = st.toggle(
                        f"Include {branch} settings",
                        branch in doc.enabled,
                        key=scope + ":enabled",
                        help="Omit this branch while remembering its edits.",
                    )
                    if enabled:
                        doc.enabled.add(branch)
                    else:
                        doc.enabled.discard(branch)
                if branch in ("Chart", "animation"):
                    prefix = reference = ""
                if branch == "graphic":
                    prefix, reference = "graphic.elements[0]", "graphic.elements-text"
                _component_bindings(branch, doc, scope, set(paths), enabled)
                values = doc.components[branch]
            rows = {
                p: (
                    sections[branch][p],
                    get_values(p) if branch == "series" else values,
                )
                for p in paths
                if sections[branch][p].kind != "binding"
            }
            _render_groups(rows, scope, prefix, reference, enabled)


def _render_groups(rows, scope, prefix, reference, enabled):
    """Keep child controls inside their parent's disclosure, in catalog order."""
    groups = defaultdict(list)
    for path in rows:
        root, separator, _ = path.partition(".")
        groups[root if separator else ""].append(path)
    for group in sorted(groups, key=bool):
        holder = (
            st.expander(group, expanded=True) if group else st.container(gap="xsmall")
        )
        with holder:
            parents = defaultdict(list)
            for path in groups[group]:
                parents[path.rpartition(".")[0]].append(path)
            for parent in sorted(parents, key=lambda parent: parent != group):
                if parent != group:
                    st.markdown(f"**`{parent}`**")
                for path in parents[parent]:
                    spec, values = rows[path]
                    _row(
                        path,
                        spec,
                        values,
                        prefix,
                        reference,
                        f"{scope}:{path}",
                        enabled,
                    )
