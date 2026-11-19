"""Editor defaults for the unthemed ECharts 6.1 renderer in Streamlit 1.67.

A None default means the property is absent and the renderer computes or inherits
its value. The placeholder explains that behaviour without inventing a literal.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Property:
    default: object
    hint: str
    kind: str
    choices: tuple = ()
    bounds: tuple = ()
    unit: str = ""
    placeholder: str = ""


def text(default, hint, placeholder=""):
    return Property(default, hint, "text", placeholder=placeholder)


def flag(default, hint):
    return Property(default, hint, "bool")


def choice(default, hint, *values, placeholder="Auto"):
    return Property(default, hint, "choice", choices=values, placeholder=placeholder)


def number(default, low, high, hint, unit="", placeholder=""):
    return Property(
        default, hint, "number", bounds=(low, high), unit=unit, placeholder=placeholder
    )


def percent(default, low, high, hint, placeholder=""):
    return Property(
        default, hint, "percent", bounds=(low, high), unit="%", placeholder=placeholder
    )


def color(default, hint, placeholder="Auto"):
    return Property(default, hint, "color", placeholder=placeholder)


def text_style(prefix, *, ink=None, size=12, weight="normal"):
    return {
        prefix + ".color": color(
            ink, "Change the text colour.", "Auto · inherited colour"
        ),
        prefix + ".fontSize": number(size, 1, 72, "Set the text size.", "px"),
        prefix + ".fontWeight": choice(
            weight, "Change the text weight.", "normal", "bold", "lighter", "bolder"
        ),
        prefix + ".fontStyle": choice(
            "normal", "Set the type style.", "normal", "italic", "oblique"
        ),
    }


def stroke(prefix, ink, width=1):
    return {
        prefix + ".color": color(ink, "Set the stroke colour.", "Auto · series colour"),
        prefix + ".width": number(width, 0, 16, "Set the stroke thickness.", "px"),
        prefix + ".type": choice(
            "solid", "Choose a stroke pattern.", "solid", "dashed", "dotted"
        ),
    }


def statistic(hint, *values):
    return Property(None, hint, "statistic", choices=values, placeholder="None")


def binding(hint):
    return Property(None, hint, "binding")


def axis_properties(axis_type):
    fields = {
        "show": flag(True, "Display the axis and its labels."),
        "name": text("", "Label the axis with a measure or unit.", "Empty"),
        "nameLocation": choice(
            "end", "Position the axis name.", "start", "middle", "end"
        ),
        "nameGap": number(15, 0, 90, "Distance between the axis and its name.", "px"),
        "nameRotate": number(
            None,
            -90,
            90,
            "Angle the axis name. ECharts otherwise follows its location.",
            "°",
            "Auto · name location",
        ),
        "inverse": flag(False, "Reverse the order along the axis."),
        **text_style("nameTextStyle"),
        "axisLabel.show": flag(True, "Display tick labels."),
        "axisLabel.rotate": number(
            0, -90, 90, "Rotate tick labels to fit long category names.", "°"
        ),
        "axisLabel.hideOverlap": flag(False, "Hide labels that would collide."),
        "axisLabel.inside": flag(False, "Move tick labels into the plotting area."),
        "axisLabel.margin": number(
            8, 0, 50, "Space between labels and the axis.", "px"
        ),
        **text_style("axisLabel", ink="#54555a"),
        "axisTick.show": choice(
            None,
            "Draw ticks at axis intervals. Auto uses the paired axis type.",
            True,
            False,
        ),
        "axisTick.inside": flag(False, "Draw ticks inside the plot."),
        "axisTick.length": number(5, 0, 30, "Adjust tick length.", "px"),
        "axisLine.show": (
            flag(True, "Display the axis baseline.")
            if axis_type == "category"
            else choice(
                None,
                "Display the baseline. Auto uses the paired axis type.",
                True,
                False,
            )
        ),
        **stroke("axisLine.lineStyle", "#54555a"),
        "splitLine.show": flag(
            axis_type == "value", "Draw grid lines through the plotting area."
        ),
        **stroke("splitLine.lineStyle", "#dbdee4"),
        "splitArea.show": flag(False, "Shade alternating bands between grid lines."),
    }
    if axis_type == "category":
        fields["boundaryGap"] = flag(
            True, "Leave half a category band at both ends of the axis."
        )
    if axis_type == "value":
        fields.update(
            {
                "min": number(
                    None,
                    None,
                    None,
                    "Set the lower bound of the numeric scale.",
                    placeholder="Auto · data extent",
                ),
                "max": number(
                    None,
                    None,
                    None,
                    "Set the upper bound of the numeric scale.",
                    placeholder="Auto · data extent",
                ),
                "scale": flag(
                    False,
                    "Let the value axis scale to the data range without requiring zero.",
                ),
                "splitNumber": number(
                    5, 1, 20, "Suggest how many intervals to use along the scale."
                ),
                "axisLabel.formatter": text(
                    None, "Use {value} in a tick label template.", "Auto · axis value"
                ),
            }
        )
    return fields


COMMON_SERIES = {
    "stack": text(
        None, "Give two series the same stack name to accumulate their values.", "None"
    ),
    "silent": flag(False, "Turn off pointer interactions for this series."),
    "itemStyle.color": color(
        None, "Set the fill colour of this series.", "Auto · series palette"
    ),
    "itemStyle.opacity": number(1.0, 0.0, 1.0, "Control the transparency of marks."),
    "itemStyle.borderColor": color(
        None,
        "Outline the marks. Increase borderWidth to see the edge.",
        "Auto · mark outline",
    ),
    "itemStyle.borderWidth": number(
        0, 0, 12, "Change the mark outline thickness.", "px"
    ),
    "label.show": flag(False, "Write a label next to each data mark."),
    "labelLayout.hideOverlap": flag(
        False, "Hide overlapping data labels, keeping higher-priority labels visible."
    ),
    "labelLayout.moveOverlap": choice(
        None,
        "Shift overlapping labels horizontally or vertically.",
        "shiftX",
        "shiftY",
        placeholder="No movement",
    ),
    "encode.tooltip": binding("Choose and order DataFrame fields in the item tooltip."),
    "label.rotate": number(0, -90, 90, "Angle mark labels.", "°"),
    "label.distance": number(
        5, 0, 40, "Adjust the gap between labels and marks.", "px"
    ),
    "label.formatter": text(
        None,
        "Use {a} for the series name or reference a field such as {@Revenue}.",
        "Auto · data value",
    ),
    **text_style("label"),
    "emphasis.focus": choice(
        "none",
        "Hover a mark to focus its series or just that mark.",
        "none",
        "series",
        "self",
    ),
    "emphasis.itemStyle.color": color(
        None, "Hover a mark to see its highlight colour.", "Auto · highlighted fill"
    ),
    "emphasis.label.show": choice(
        None,
        "Reveal or hide the data label on hover.",
        True,
        False,
        placeholder="Auto · normal label",
    ),
    "markLine.data": binding(
        "Add named reference lines for an average, median, minimum, maximum or fixed axis threshold."
    ),
    "markArea.data": binding(
        "Shade a reference band between two axis values or dates."
    ),
    "datasetIndex": binding(
        "Calculate a linear regression trend line or a trailing moving average from this series."
    ),
    "markLine.label.show": flag(
        True, "Show a label on the reference line when markLine.data is set."
    ),
    "markPoint.data": statistic(
        "Annotate the minimum or maximum observation.", "min", "max"
    ),
    "markPoint.label.formatter": text(
        None,
        "Label a marked peak or minimum. Use {b} for its name and {c} for its value.",
        "Auto · marked value",
    ),
    "markPoint.symbolSize": number(
        50, 1, 100, "Resize the marker created by markPoint.data.", "px"
    ),
}


def label_position(default):
    return choice(
        default,
        "Place labels relative to marks.",
        "top",
        "bottom",
        "inside",
        "left",
        "right",
        "insideTop",
        "insideBottom",
        "insideLeft",
        "insideRight",
    )


BAR = {
    "barWidth": percent(
        None,
        1,
        100,
        "Set the bar width within its category band.",
        "Auto · available space",
    ),
    # ECharts 6.1 BaseBarSeries.defaultBarGap and layout/barGrid.js.
    "barGap": percent(
        "10%",
        -100,
        150,
        "Space between bars in the same category. Edit the last bar series for the shared layout.",
    ),
    "barCategoryGap": percent(
        None,
        0,
        95,
        "Space between groups of bars in adjacent categories. Edit the last bar series for the shared layout.",
        "Auto · group count",
    ),
    "barMaxWidth": percent(
        None, 1, 100, "Limit how wide a bar can grow in its category.", "No limit"
    ),
    "barMinHeight": number(
        0, 0, 30, "Give very small bars a visible minimum height.", "px"
    ),
    "showBackground": flag(False, "Draw a track behind each bar."),
    "backgroundStyle.color": color(
        "rgba(180, 180, 180, 0.2)",
        "Change the track colour when showBackground is enabled.",
    ),
    "itemStyle.borderRadius": number(0, 0, 40, "Round the corners of bars.", "px"),
    "label.position": label_position("inside"),
    "z": number(2, 0, 20, "Draw higher values in front of overlapping series."),
}
LINE = {
    "smooth": flag(False, "Curve the line between observations."),
    "connectNulls": flag(
        False, "Bridge missing observations. Try High in the Weather log."
    ),
    "step": choice(
        False, "Place a step between adjacent values.", False, "start", "middle", "end"
    ),
    "showSymbol": flag(True, "Display point markers along the line."),
    "symbol": choice(
        "emptyCircle",
        "Choose the point marker shape.",
        "emptyCircle",
        "circle",
        "rect",
        "roundRect",
        "triangle",
        "diamond",
        "pin",
        "arrow",
        "none",
    ),
    "symbolSize": number(6, 1, 32, "Set the marker size.", "px"),
    "label.position": label_position("top"),
    "areaStyle.opacity": number(
        None,
        0.0,
        1.0,
        "Set an opacity to fill the area beneath the line. An area with only a colour uses 0.7.",
        placeholder="Auto · area style",
    ),
    "areaStyle.color": color(
        None, "Choose the fill under the line.", "Auto · series colour"
    ),
    "endLabel.show": flag(False, "Place a label at the end of the line."),
    **stroke("lineStyle", None, width=2),
    "z": number(3, 0, 20, "Draw higher values in front of overlapping series."),
}

SCATTER = {
    "symbol": choice(
        "circle", "Choose the point marker shape.", *LINE["symbol"].choices
    ),
    "symbolSize": number(
        10,
        1,
        80,
        "Set a fixed marker size. A visualMap can vary the size by a numeric column.",
        "px",
    ),
    "symbolRotate": number(
        0, -180, 180, "Rotate markers such as triangles or diamonds.", "°"
    ),
    "itemStyle.opacity": number(
        0.8, 0.0, 1.0, "Reveal overlapping points by changing their opacity."
    ),
    "label.position": label_position("inside"),
    "z": number(2, 0, 20, "Draw higher values in front of overlapping series."),
}
HEATMAP = {
    "itemStyle.borderRadius": number(
        0, 0, 40, "Round the corners of each heatmap cell.", "px"
    ),
    "label.position": label_position("inside"),
    "z": number(2, 0, 20, "Draw higher values in front of overlapping series."),
}

SERIES_SPECIFIC = {"bar": BAR, "line": LINE, "scatter": SCATTER, "heatmap": HEATMAP}

SERIES_FIELDS = {
    "bar": BAR | COMMON_SERIES,
    "line": LINE | COMMON_SERIES,
    "scatter": SCATTER
    | {k: v for k, v in COMMON_SERIES.items() if k not in SCATTER and k != "stack"},
    "heatmap": HEATMAP
    | {
        k: v
        for k, v in COMMON_SERIES.items()
        if k not in ("stack", "itemStyle.color", "datasetIndex")
        and not k.startswith(("markLine.", "markArea.", "markPoint."))
    },
}

VISUAL_MAP_STYLE = {
    "show": flag(
        True, "Show the scale legend. Hiding it keeps the visual mapping active."
    ),
    "calculable": flag(
        False, "Drag the scale handles to highlight a range of observations."
    ),
    "orient": choice("vertical", "Lay out the scale legend.", "vertical", "horizontal"),
    "left": choice(
        None,
        "Position the scale legend horizontally.",
        "left",
        "center",
        "right",
        placeholder="Left edge · 0 px",
    ),
    "inverse": flag(False, "Reverse the direction of the scale legend."),
}


def visual_map_fields(kind):
    # These bindings are written explicitly, including the data-derived domain.
    channel = (
        ("inRange.color", "Choose colours for the lowest and highest cell values.")
        if kind == "heatmap"
        else (
            "inRange.symbolSize",
            "Map low and high values to marker sizes in pixels.",
        )
    )
    return (
        {
            path: Property(None, hint, "binding")
            for path, hint in (
                ("seriesIndex", "Choose which series receives the mapping."),
                (
                    "dimension",
                    "Select the numeric DataFrame column that drives point size or cell colour.",
                ),
                ("min", "Set the low end of the mapping domain."),
                ("max", "Set the high end of the mapping domain."),
                channel,
            )
        }
        | (
            {
                "type": binding("Use continuous colours or piecewise sales bands."),
                "pieces": binding(
                    "Edit the thresholds, labels and colours of individual bands."
                ),
            }
            if kind == "heatmap"
            else {}
        )
        | VISUAL_MAP_STYLE
    )


COMPONENTS = {
    "dataset": {
        "transform": binding(
            "Filter source rows by a field, operator and value. Sort or rank the plotted rows."
        )
    },
    "Chart": {
        "backgroundColor": color(
            None, "Paint the whole chart canvas, including its margins.", "Transparent"
        ),
        "color": binding("Set and reorder the global series colour palette."),
        "textStyle.fontFamily": choice(
            "sans-serif",
            "Choose the inherited chart typeface.",
            "sans-serif",
            "serif",
            "monospace",
            "Arial",
            "Georgia",
        ),
        "textStyle.fontSize": number(
            12, 6, 48, "Set the base font size for text that inherits it.", "px"
        ),
    },
    "grid": {
        edge: Property(
            default,
            f"Inset the plot from the {edge}. Enter pixels or a percentage.",
            "length",
        )
        for edge, default in (
            ("left", "15%"),
            ("right", "10%"),
            ("top", 65),
            ("bottom", 80),
        )
    }
    | {
        "show": flag(False, "Paint the Cartesian plot background and border."),
        "backgroundColor": color(
            "rgba(0,0,0,0)",
            "Set the colour inside the plot. Enable grid.show to see it.",
        ),
        "borderColor": color(
            "#b7b9be", "Set the outline colour when grid.show is enabled."
        ),
        "borderWidth": number(1, 0, 16, "Set the plot border thickness.", "px"),
        "outerBoundsMode": choice(
            "auto",
            "Constrain long axis labels to the grid rectangle with same, or let them overflow with none.",
            "auto",
            "same",
            "none",
        ),
        "outerBoundsContain": choice(
            "all",
            "Choose whether the outer bounds include axis labels and axis names.",
            "all",
            "axisLabel",
            "auto",
        ),
        "gridIndex": binding(
            "Arrange one panel per series with grid arrays and axis gridIndex."
        ),
        "axisPointer.link": binding(
            "Link pointers across panels that share a dimension."
        ),
    },
    "tooltip": {
        "order": choice(
            None,
            "Order series in an axis-triggered tooltip by series or by value.",
            "seriesAsc",
            "seriesDesc",
            "valueAsc",
            "valueDesc",
            placeholder="Auto · series order",
        ),
        "trigger": choice(
            "item", "Inspect one mark or a whole axis position.", "item", "axis", "none"
        ),
        "axisPointer.type": choice(
            "line",
            "Guide the pointer across an axis.",
            "line",
            "shadow",
            "cross",
            "none",
        ),
        "confine": choice(
            None,
            "Keep the tooltip inside the chart. Auto follows the rendering mode.",
            True,
            False,
        ),
        "backgroundColor": color("#ffffff", "Set the tooltip panel colour."),
        **text_style("textStyle", ink="#6d6e73", size=14),
    },
    "legend": {
        "padding": number(5, 0, 60, "Add space around the legend entries.", "px"),
        "backgroundColor": color("rgba(0,0,0,0)", "Paint the legend box."),
        "orient": choice(
            "horizontal",
            "Arrange series names in a row or column.",
            "horizontal",
            "vertical",
        ),
        "left": choice(
            "center", "Align the legend horizontally.", "center", "left", "right"
        ),
        "top": percent(
            None,
            0,
            100,
            "Position the legend vertically. ECharts anchors it near the bottom by default.",
            "Auto · bottom aligned",
        ),
        "itemGap": number(8, 0, 60, "Set the space between legend entries.", "px"),
        "selectedMode": choice(
            True,
            "Control series selection by clicking legend entries.",
            True,
            False,
            "single",
            "multiple",
        ),
        **text_style("textStyle", ink="#54555a"),
    },
    "title": {
        "top": Property(
            15, "Place the heading vertically using pixels or a percentage.", "length"
        ),
        "padding": number(5, 0, 60, "Add space inside the title box.", "px"),
        "itemGap": number(
            10, 0, 70, "Adjust the gap between title and subtitle.", "px"
        ),
        "backgroundColor": color(
            "rgba(0,0,0,0)", "Paint the title box behind both lines."
        ),
        "text": text("", "Set the chart title.", "Empty"),
        "subtext": text("", "Add a subtitle beneath the title.", "Empty"),
        "left": choice(
            "center", "Align the title horizontally.", "center", "left", "right"
        ),
        **text_style("textStyle", ink="#3c3c41", size=18, weight="bold"),
        **text_style("subtextStyle", ink="#86878c"),
    },
    "dataZoom": {
        "type": choice(
            "slider",
            "Use a visible range slider or zoom inside the chart.",
            "slider",
            "inside",
        ),
        "start": number(
            0, 0, 100, "Start of the visible window, as a numeric percentage.", "%"
        ),
        "end": number(
            100, 0, 100, "End of the visible window, as a numeric percentage.", "%"
        ),
        "filterMode": choice(
            "filter",
            "Filter rows outside the visible window.",
            "filter",
            "weakFilter",
            "empty",
            "none",
        ),
    },
    "animation": {
        "animation": choice(
            None,
            "Enable or disable animation. Auto accounts for the rendering environment.",
            True,
            False,
        ),
        "animationDuration": number(
            1000, 0, 3000, "Duration when marks first appear.", "ms"
        ),
        "animationDurationUpdate": number(
            500, 0, 3000, "Duration for changes to existing marks.", "ms"
        ),
        "animationEasingUpdate": choice(
            "cubicInOut",
            "Control the pacing of updated marks.",
            "cubicInOut",
            "cubicOut",
            "linear",
            "bounceOut",
            "elasticOut",
        ),
    },
    "graphic": {
        "elements": binding(
            "Pin a text annotation or source note to a corner of the canvas."
        ),
        "style.text": text(
            "",
            "Write the note that stays in place when the chart zooms.",
            "Source note",
        ),
        "style.fill": color("#000000", "Set the note text colour."),
        "style.fontSize": number(12, 6, 48, "Set the note text size.", "px"),
    },
    "media": {
        "query": binding(
            "Add responsive layout rules for preview width, height or aspect ratio."
        ),
        "option.legend": binding("Reposition the legend when a breakpoint matches."),
        "option.grid": binding("Change a horizontal grid inset at a breakpoint."),
    },
    "toolbox": {
        "feature.dataZoom": Property(
            False, "Add drag-to-zoom and zoom-back tools.", "feature"
        ),
        "feature.restore": Property(
            False, "Restore the original chart interaction state.", "feature"
        ),
        "orient": choice(
            "horizontal", "Lay out the toolbar icons.", "horizontal", "vertical"
        ),
        "left": choice(
            "right", "Place the toolbar horizontally.", "left", "center", "right"
        ),
        "top": choice(
            "top", "Place the toolbar vertically.", "top", "middle", "bottom"
        ),
    },
    "brush": {
        "toolbox": binding(
            "Select rectangular or polygon brushes in the chart toolbar."
        ),
        "brushMode": choice(
            "single",
            "Keep one selection or build up several areas.",
            "single",
            "multiple",
        ),
        "inBrush.color": color(None, "Highlight selected marks.", "Original colour"),
        "inBrush.opacity": number(
            None,
            0.0,
            1.0,
            "Adjust the opacity of selected marks.",
            placeholder="Series opacity",
        ),
        "outOfBrush.color": color(
            "#cfd2d7", "Set the colour of marks outside the selection."
        ),
        "outOfBrush.opacity": number(
            None,
            0.0,
            1.0,
            "Fade marks outside the selection.",
            placeholder="Series opacity",
        ),
    },
    "aria": {
        "label.description": text(
            "", "Describe this chart for a screen reader.", "Auto · describe the chart"
        ),
        "decal.show": flag(
            False, "Add patterns so series can be distinguished without colour."
        ),
    },
}
OPTIONAL_BRANCHES = tuple(k for k in COMPONENTS if k not in ("Chart", "dataset"))


def catalog(kind, x_type, multiple_x=False, *, mapping_kind=None, y_type=None):
    x_fields = axis_properties(x_type)
    x_fields["position"] = choice(
        None,
        "Choose the horizontal axis edge.",
        "bottom",
        "top",
        placeholder="Auto · available edge" if multiple_x else "Auto · bottom edge",
    )
    y_fields = axis_properties(y_type or ("category" if kind == "heatmap" else "value"))
    x_fields["type"] = y_fields["type"] = binding(
        "Show the data scale and change which axis encodes the dimension."
    )
    if kind == "heatmap":
        # Cartesian heatmap cells need bands along both category axes.
        x_fields.pop("boundaryGap", None)
        y_fields.pop("boundaryGap", None)
    y_fields["position"] = choice(
        "left", "Choose the vertical axis edge.", "left", "right"
    )
    return {
        "series": SERIES_FIELDS[kind],
        "xAxis": x_fields,
        "yAxis": y_fields,
        **({"visualMap": visual_map_fields(mapping_kind)} if mapping_kind else {}),
        **COMPONENTS,
    }


def matches(sections, query):
    words = query.lower().replace(".", " ").split()
    return [
        (section, path)
        for section, fields in sections.items()
        for path, prop in fields.items()
        if all(word in f"{section} {path} {prop.hint}".lower() for word in words)
    ]
