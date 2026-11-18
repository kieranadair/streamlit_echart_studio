"""Direct-edit controls for the active option branch."""

from collections import defaultdict
from collections.abc import Callable
from typing import Literal, TypedDict

import streamlit as st

from .options import axis_type
from .schema import OPTIONAL_BRANCHES, catalog, matches


def data_bindings(doc, frame, sample, key):
    x_col, y_col = st.columns(2)
    columns = frame.columns.tolist()
    doc.shared_x = x_col.selectbox(
        "Shared X field · encode.x",
        columns,
        index=columns.index(doc.shared_x),
        key=key + ":shared-x",
        help="Each series uses this column unless you override encode.x in the series tab.",
    )
    doc.measures = y_col.multiselect(
        "Y fields · encode.y",
        sample.measures,
        default=doc.measures,
        key=key + ":measures",
        help="Each selected measure creates one series. Its encode.y names this DataFrame column.",
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
    kinds = ["bar", "line"]
    col2.selectbox(
        "series.type",
        kinds,
        index=kinds.index(series.kind),
        key=type_key,
        on_change=_write_attribute,
        args=(series, "kind", type_key),
    )
    x_key = f"{key}:{measure}:encode.x"
    fields = [None, *frame.columns]
    col3.selectbox(
        "encode.x",
        fields,
        index=fields.index(series.x_override),
        key=x_key,
        format_func=lambda column: (
            f"Shared · {doc.shared_x}" if column is None else column
        ),
        on_change=_write_attribute,
        args=(series, "x_override", x_key),
        help="Use a separate X field for this series. Each distinct X field gets its own horizontal axis.",
    )


def _literal(value):
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _widget_value(spec, value):
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


def _sync(key, value):
    # The document owns edits across hidden tabs. A reset only changes the
    # document; bring its widget back into sync before registering the widget.
    if key not in st.session_state or st.session_state[key] != value:
        st.session_state[key] = value


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
    elif spec.kind == "bool":
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
    x_fields = doc.x_fields()
    x_field = _focused(key + ":axis", x_fields)
    sections = catalog(
        series.kind if series else "bar", axis_type(frame[x_field]), len(x_fields) > 1
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
        with tab, st.container(height=505, border=False):
            enabled = True
            if branch == "series":
                if series is None:
                    st.info("Choose a Y field above to create a series.")
                    continue
                _series_controls(doc, measure, frame, key)
                scope = f"{key}:series:{measure}:{series.kind}"
                prefix = f"series[{doc.measures.index(measure)}]"
                reference = f"series-{series.kind}"
            elif branch == "xAxis":
                if len(x_fields) > 1:
                    st.selectbox(
                        "Edit X axis",
                        x_fields,
                        index=x_fields.index(x_field),
                        key=key + ":axis",
                        persist_state="page",
                    )
                scope = f"{key}:xAxis:{x_field}"
                prefix = (
                    f"xAxis[{x_fields.index(x_field)}]"
                    if len(x_fields) > 1
                    else "xAxis"
                )
                reference = "xAxis"
                st.caption(
                    f"`encode.x = {x_field!r}` · `{prefix}.type = {axis_type(frame[x_field])!r}`"
                )
            else:
                scope = f"{key}:{branch}"
                prefix = reference = "" if branch == "animation" else branch
                if branch in OPTIONAL_BRANCHES:
                    enabled = st.toggle(
                        f"Include {branch} settings",
                        branch in doc.enabled,
                        key=f"{key}:{branch}:enabled",
                        help="Omit this branch while remembering its edits.",
                    )
                    if enabled:
                        doc.enabled.add(branch)
                    else:
                        doc.enabled.discard(branch)

            rows = {}
            for section, path in visible:
                if section != branch:
                    continue
                if branch == "series":
                    values = series.settings(path)
                elif branch == "xAxis":
                    values = doc.axes[x_field]
                else:
                    values = doc.components[branch]
                rows[path] = (sections[branch][path], values)
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
