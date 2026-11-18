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
    "markLine.data": statistic(
        "Draw a reference line for a statistic of this series.",
        "average",
        "median",
        "min",
        "max",
    ),
    "markLine.label.show": flag(
        True, "Show a label on the reference line when markLine.data is set."
    ),
    "markPoint.data": statistic(
        "Annotate the minimum or maximum observation.", "min", "max"
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

COMPONENTS = {
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
    },
    "tooltip": {
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
}
OPTIONAL_BRANCHES = tuple(COMPONENTS)


def catalog(kind, x_type, multiple_x=False):
    x_fields = axis_properties(x_type)
    x_fields["position"] = choice(
        None,
        "Choose the horizontal axis edge.",
        "bottom",
        "top",
        placeholder="Auto · available edge" if multiple_x else "Auto · bottom edge",
    )
    y_fields = axis_properties("value")
    y_fields["position"] = choice(
        "left", "Choose the vertical axis edge.", "left", "right"
    )
    return {
        "series": (BAR if kind == "bar" else LINE) | COMMON_SERIES,
        "xAxis": x_fields,
        "yAxis": y_fields,
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
