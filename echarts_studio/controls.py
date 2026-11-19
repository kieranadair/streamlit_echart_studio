"""Native controls for repeatable option items and data-dependent field bindings."""

from datetime import date

import streamlit as st

from .datasets import axis_type
from .layers import LEGEND_PLACEMENTS, ColourBand, MediaRule, Reference, coordinate


def sync(key, value):
    if key not in st.session_state or st.session_state[key] != value:
        st.session_state[key] = value


def select(box, label, choices, value, key, **kwargs):
    return box.selectbox(label, choices, index=choices.index(value), key=key, **kwargs)


def axis_value(box, label, column, value, key, *, discrete=False):
    kind = axis_type(column)
    if discrete or kind == "category":
        if kind == "time":
            values = [d.isoformat() for d in column.dropna().dt.date.unique()]
            value = str(value)[:10]
        else:
            values = [coordinate(v) for v in column.dropna().unique()]
        return select(box, label, values, value if value in values else values[0], key)
    if kind == "value":
        return box.number_input(label, value=float(value), key=key)
    picked = box.date_input(label, value=date.fromisoformat(str(value)[:10]), key=key)
    return picked.isoformat()


def dataset_controls(doc, frame, key):
    transform = doc.transform
    none = "None"
    fields = [none, *frame.columns]
    st.caption(
        "The source DataFrame stays in dataset[0]. A filter or sort creates dataset[1] for the plotted rows."
    )
    col, op = st.columns(2)
    selected = select(
        col,
        "Filter field · dimension",
        fields,
        transform.filter_field or none,
        key + ":filter",
    )
    column = None if selected == none else selected
    if column != transform.filter_field:
        transform.filter_field = column
        if column is not None:
            data = frame[column].dropna()
            transform.operator = "eq" if axis_type(data) == "category" else "gte"
            transform.value = coordinate(data.iloc[0])
    if column is not None:
        values = frame[column]
        operators = (
            ["eq", "ne"]
            if axis_type(values) == "category"
            else ["gte", "gt", "lte", "lt", "eq"]
        )
        transform.operator = select(
            op, "Filter operator", operators, transform.operator, f"{key}:op:{column}"
        )
        transform.value = axis_value(
            st, "Filter value", values, transform.value, f"{key}:filter-value:{column}"
        )
    col, order = st.columns(2)
    selected = select(
        col,
        "Sort field · dimension",
        fields,
        transform.sort_field or none,
        key + ":sort",
    )
    transform.sort_field = None if selected == none else selected
    transform.order = select(
        order,
        "Sort order",
        ["asc", "desc"],
        transform.order,
        key + ":order",
        disabled=not transform.sort_field,
    )


def _seed_reference(kind, field, values):
    data = values.dropna()
    lo, hi = coordinate(data.iloc[0]), coordinate(data.iloc[-1])
    if axis_type(data) == "value":
        lo, hi = float(data.median()), float(data.max())
    return Reference(kind, field, lo, hi)


def _reference_item(ref, series, x, y, frame, key, scales):
    key = f"{key}:{ref.uid}"
    a, b = st.columns(2)
    previous_kind = ref.kind
    if ref.kind != "Band":
        ref.kind = select(
            a, "Line definition", ["Fixed", "Statistic"], ref.kind, key + ":kind"
        )
    labels = {x: f"{x} · xAxis", y: f"{y} · yAxis"}
    if x == y:
        labels[x] = f"{x} · both axes"
    fields = list(
        dict.fromkeys(
            field
            for axis, field in (("xAxis", x), ("yAxis", y))
            if ref.kind != "Statistic" or scales[axis] == "value"
        )
    )
    initial = ref.column
    if initial not in fields:
        if previous_kind != ref.kind and fields:
            initial = fields[0]
        else:
            fields.append(initial)
            st.caption(
                "Statistical lines need a value axis. Choose a numeric binding or a fixed line."
                if initial in (x, y)
                else f"{initial} is currently unbound. Select an active axis to draw this reference."
            )
    field = select(
        b if ref.kind != "Band" else a,
        "Axis field",
        fields,
        initial,
        key + ":field",
        format_func=lambda f: labels.get(f, f),
    )
    if field != ref.column:
        ref.column = field
        seed = _seed_reference(ref.kind, field, frame[field])
        ref.start, ref.end = seed.start, seed.end
    if x == y == field and ref.kind != "Statistic":
        ref.axis_when_shared = select(
            st,
            "Reference axis",
            ["xAxis", "yAxis"],
            ref.axis_when_shared,
            key + ":axis",
        )
    discrete = scales[ref.axis(x, y)] == "category" and field in (x, y)
    col1, col2 = st.columns(2)
    if ref.kind == "Statistic":
        ref.statistic = select(
            col1,
            "Statistic · type",
            ["average", "median", "min", "max"],
            ref.statistic,
            key + ":stat",
        )
    else:
        ref.start = axis_value(
            col1,
            "From" if ref.kind == "Band" else "Axis value",
            frame[field],
            ref.start,
            f"{key}:from:{field}:{discrete}",
            discrete=discrete,
        )
    if ref.kind == "Band":
        ref.end = axis_value(
            col2,
            "To",
            frame[field],
            ref.end,
            f"{key}:to:{field}:{discrete}",
            discrete=discrete,
        )
    name_box = st if ref.kind == "Band" else col2
    ref.name = name_box.text_input(
        "Label · name", value=ref.name, key=key + ":name", placeholder="Optional"
    )
    with st.container(horizontal=True, vertical_alignment="center"):
        with st.popover("Style"):
            ref.colour = st.color_picker(
                "Colour", ref.colour, key=key + ":colour"
            ).lower()
            if ref.kind == "Band":
                ref.opacity = st.slider(
                    "itemStyle.opacity", 0.0, 1.0, ref.opacity, key=key + ":opacity"
                )
            else:
                ref.width = st.slider(
                    "lineStyle.width", 1, 12, ref.width, key=key + ":width"
                )
                ref.dash = select(
                    st,
                    "lineStyle.type",
                    ["solid", "dashed", "dotted"],
                    ref.dash,
                    key + ":dash",
                )
        st.button(
            "Remove",
            key=key + ":remove",
            on_click=series.references.remove,
            args=(ref,),
        )


def series_bindings(doc, measure, frame, key, paths, expanded):
    series = doc.series[measure]
    x, y = doc.bindings(measure)
    scales = {
        axis: doc.axis_kind(axis, doc.x_for(measure), frame)
        for axis in ("xAxis", "yAxis")
    }
    if "encode.tooltip" in paths or "label.formatter" in paths:
        with st.expander("Data labels and hover fields", expanded=expanded):
            if "label.formatter" in paths:
                widget_label = key + ":label-field"
                automatic = "Use label.formatter"
                templates = {"{@" + col + "}": col for col in frame.columns}
                sync(
                    widget_label,
                    templates.get(series.common.get("label.formatter"), automatic),
                )

                def label_field():
                    col = st.session_state[widget_label]
                    if col == automatic:
                        series.common.pop("label.formatter", None)
                    else:
                        series.common.update(
                            {"label.formatter": "{@" + col + "}", "label.show": True}
                        )

                st.selectbox(
                    "Label with a field",
                    [automatic, *frame.columns],
                    key=widget_label,
                    on_change=label_field,
                    help="Choosing a field sets label.show and creates a named-dimension label.formatter.",
                )
            if "encode.tooltip" in paths:
                tooltip_fields(series, doc.item_name, x, y, frame, key)
    if "datasetIndex" in paths:
        with st.expander(
            "Calculated trend · datasetIndex",
            expanded=expanded or series.trend != "None",
        ):
            methods = doc.trend_methods(measure, frame)
            if series.trend not in methods:
                methods.append(series.trend)
            series.trend = select(
                st, "Trend calculation", methods, series.trend, key + ":trend"
            )
            if series.trend == "Moving average":
                series.window = st.number_input(
                    "Trailing window (observations)",
                    min_value=2,
                    max_value=60,
                    value=series.window,
                    key=key + ":window",
                )
                st.caption(
                    "Each point averages a full window in dimension order. A missing reading leaves a gap until the next complete window."
                )
            elif series.trend == "Linear fit":
                st.caption(
                    "A linear fit uses least squares over the plotted numeric pairs. Inspect the two fitted endpoints under the data bindings."
                )
            else:
                st.caption(
                    "Trend choices follow the bound fields and axis types. Try a numeric dimension for a linear fit, or Month for a trailing average."
                )
    for path, band in (("markLine.data", False), ("markArea.data", True)):
        if path not in paths:
            continue
        title = "Reference bands" if band else "Reference lines"
        items = [r for r in series.references if (r.kind == "Band") == band]
        with st.expander(
            f"{title} · {path} ({len(items)})", expanded=expanded or bool(items)
        ):
            for ref in items:
                with st.container(border=True):
                    _reference_item(ref, series, x, y, frame, key, scales)
            field = doc.x_for(measure) if band else measure

            def add_reference(field=field, band=band):
                series.references.append(
                    _seed_reference("Band" if band else "Fixed", field, frame[field])
                )

            st.button(
                "Add reference band" if band else "Add reference line",
                key=key + ":" + path + ":add",
                on_click=add_reference,
            )


def tooltip_fields(series, item_name, x, y, frame, key):
    default = (
        list(
            dict.fromkeys(
                [item_name, x, y]
                + ([series.mapping.dimension] if series.mapping.dimension else [])
            )
        )
        if series.kind == "scatter"
        else []
    )
    current = default if series.tooltip_fields is None else series.tooltip_fields
    widget = key + ":tooltip-fields"
    sync(widget, current)

    def update_fields():
        selected = st.session_state[widget]
        series.tooltip_fields = selected if selected != default else None

    st.multiselect(
        "Tooltip fields in display order",
        frame.columns,
        key=widget,
        on_change=update_fields,
        help="Select columns in the order you want to see them on hover.",
    )
    if series.tooltip_fields is not None:
        st.button(
            "Use automatic fields",
            key=widget + ":reset",
            on_click=setattr,
            args=(series, "tooltip_fields", None),
        )


def _change_cutoff(bands, i, widget):
    value = st.session_state[widget]
    lower = bands[i - 1].upper if i else None
    upper = bands[i + 1].upper
    if (
        value is not None
        and (lower is None or lower < value)
        and (upper is None or value < upper)
    ):
        bands[i].upper = value
    else:
        st.toast("Each cutoff must fall between its neighbours.")


def piece_controls(mapping, frame, field, key):
    bands = mapping.bands_for(frame, field)
    st.caption("Each cutoff is inclusive. The next band starts immediately above it.")
    for i, band in enumerate(bands):
        col, threshold, colour = st.columns([1.15, 1, 0.6], vertical_alignment="bottom")
        row = f"{key}:piece:{band.uid}"
        band.label = col.text_input(
            f"Band {i + 1} label", band.label, key=row + ":label"
        )
        if band.upper is not None:
            widget = row + ":limit"
            sync(widget, band.upper)
            threshold.number_input(
                "Upper cutoff · lte",
                value=None,
                key=widget,
                on_change=_change_cutoff,
                args=(bands, i, widget),
            )
        else:
            threshold.caption("Above the last cutoff" if i else "All values")
        band.colour = colour.color_picker(
            "Colour", band.colour, key=row + ":colour"
        ).lower()
        if band.upper is not None:
            st.button(
                f"Remove band {i + 1}",
                key=row + ":remove",
                type="tertiary",
                on_click=bands.remove,
                args=(band,),
            )

    def add_band():
        low, high = mapping.data_range(frame[field])
        lower = bands[-2].upper if len(bands) > 1 else low
        cut = (lower + high) / 2 if lower < high else lower + max(1, (high - low) / 3)
        bands.insert(-1, ColourBand("New band", "#568db8", cut))

    st.button("Add colour band", key=key + ":add-piece", on_click=add_band)


def layout_controls(doc, key, enabled):
    count = len(doc.measures)
    doc.panels = st.toggle(
        "One grid per series",
        doc.panels,
        key=key + ":panels",
        disabled=not enabled,
        help="Each series gets a grid with its own xAxis and yAxis.",
    )
    if doc.panels:
        if count < 2:
            st.caption("Select two or more measures to see separate panels.")
        doc.panel_gap = st.slider(
            "Gap between panels (%)",
            1,
            18,
            doc.panel_gap,
            key=key + ":gap",
            disabled=not enabled,
        )
        doc.link_pointers = st.toggle(
            "Link shared axes · axisPointer.link",
            doc.link_pointers,
            key=key + ":link",
            disabled=not enabled,
        )
        st.caption("Panels with the same dimension can share a hover pointer.")


def media_controls(doc, key, enabled):
    st.caption(
        "Matching rules apply in list order. Resize the live chart to cross a breakpoint."
    )
    for i, rule in enumerate(doc.media_rules):
        row = f"{key}:{rule.uid}"
        with st.container(border=True):
            a, b = st.columns(2)
            condition = select(
                a,
                f"Rule {i + 1} · media.query",
                [
                    "maxWidth",
                    "minWidth",
                    "maxHeight",
                    "minHeight",
                    "maxAspectRatio",
                    "minAspectRatio",
                ],
                rule.condition,
                row + ":condition",
                disabled=not enabled,
            )
            ratio = condition.endswith("Ratio")
            if ratio != rule.condition.endswith("Ratio"):
                rule.limit = 1.0 if ratio else 500
            rule.condition = condition
            rule.limit = b.number_input(
                "Aspect ratio" if ratio else "Breakpoint (px)",
                min_value=0.1 if ratio else 1,
                value=float(rule.limit) if ratio else int(rule.limit),
                step=0.1 if ratio else 10,
                key=row + (":ratio" if ratio else ":px"),
                disabled=not enabled,
            )
            rule.placement = select(
                st,
                "Legend when matched",
                list(LEGEND_PLACEMENTS),
                rule.placement,
                row + ":legend",
                disabled=not enabled,
            )
            side, width = st.columns(2)
            edge = select(
                side,
                "Override grid inset",
                ["None", "left", "right"],
                rule.grid_edge or "None",
                row + ":edge",
                disabled=not enabled,
            )
            rule.grid_edge = None if edge == "None" else edge
            if rule.grid_edge:
                rule.inset = width.slider(
                    f"grid.{edge} (%)",
                    0,
                    60,
                    rule.inset,
                    key=row + ":inset",
                    disabled=not enabled,
                )
            st.button(
                "Remove rule",
                key=row + ":remove",
                on_click=doc.media_rules.remove,
                args=(rule,),
                disabled=not enabled,
            )
    st.button(
        "Add layout rule",
        key=key + ":add",
        on_click=doc.media_rules.append,
        args=(MediaRule(),),
        disabled=not enabled,
    )


def palette_controls(settings, key):
    palette = settings.get("color", [])
    st.caption(
        "Colours are assigned to series in order. A series colour or visualMap can override its palette colour."
    )

    def change(i, widget):
        palette[i] = st.session_state[widget].lower()

    def remove(i):
        palette.pop(i)
        if not palette:
            settings.pop("color", None)

    def earlier(i):
        palette[i - 1], palette[i] = palette[i], palette[i - 1]

    for i, value in enumerate(palette):
        widget = f"{key}:swatch:{i}"
        sync(widget, value)
        with st.container(horizontal=True, vertical_alignment="bottom"):
            st.color_picker(
                f"color[{i}]", key=widget, on_change=change, args=(i, widget)
            )
            st.button(
                "Move earlier",
                key=widget + ":up",
                disabled=i == 0,
                on_click=earlier,
                args=(i,),
            )
            st.button("Remove", key=widget + ":remove", on_click=remove, args=(i,))
    if palette:
        with st.container(horizontal=True):
            st.button(
                "Add colour",
                key=key + ":add",
                on_click=palette.append,
                args=("#4d9d8c",),
            )
            st.button(
                "Use native palette",
                key=key + ":reset",
                on_click=settings.pop,
                args=("color", None),
            )
    else:
        st.button(
            "Configure palette",
            key=key + ":start",
            on_click=settings.update,
            args=({"color": ["#326a95", "#dd8b45", "#569780"]},),
        )


def preview_size(doc, key):
    with st.popover("Preview size", icon=":material/aspect_ratio:"):
        widths = [260, 320, 400, 480, 500, 560, 640, 800, "Fit column"]
        width = st.select_slider(
            "Preview width",
            options=widths,
            value=doc.preview_width or "Fit column",
            format_func=lambda w: f"{w} px" if isinstance(w, int) else w,
            key=key + ":preview-width",
        )
        doc.preview_width = None if width == "Fit column" else width
        doc.preview_height = st.slider(
            "Preview height (px)",
            320,
            920,
            doc.preview_height,
            20,
            key=key + ":preview-height",
        )
        st.caption(
            "Streamlit sizes the chart within the available column. ECharts media queries use its rendered dimensions."
        )
