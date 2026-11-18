"""Editable JSON-compatible ECharts properties. Seeds are example values for adding a field."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Property:
    seed: object
    hint: str
    choices: tuple = ()
    bounds: tuple = ()
    unit: str = ""


def choice(hint, *values):
    return Property(values[0], hint, choices=values)


def number(seed, low, high, hint, unit=""):
    return Property(seed, hint, bounds=(low, high), unit=unit)


def color(hint, seed="#4058B9"):
    return Property(seed, hint, unit="color")


def percent(seed, low, high, hint):
    return number(f"{seed}%", low, high, hint, "%")


def text_style(prefix):
    return {
        prefix + ".color": color("Change the text colour.", "#364155"),
        prefix + ".fontSize": number(14, 8, 56, "Set the text size.", "px"),
        prefix + ".fontWeight": choice(
            "Change the text weight.", "bold", "normal", "lighter", "bolder"
        ),
        prefix + ".fontStyle": choice(
            "Set the type style.", "italic", "normal", "oblique"
        ),
    }


def stroke(prefix):
    return {
        prefix + ".color": color("Set the stroke colour."),
        prefix + ".width": number(2, 0, 16, "Set the stroke thickness.", "px"),
        prefix + ".type": choice(
            "Choose a stroke pattern.", "dashed", "solid", "dotted"
        ),
    }


AXIS = {
    "name": Property("Units", "Label the axis with a measure or unit."),
    "nameLocation": choice("Position the axis name.", "middle", "start", "end"),
    "nameGap": number(30, 0, 90, "Distance between the axis and its name.", "px"),
    "inverse": Property(True, "Reverse the order along the axis."),
    "show": Property(False, "Hide or show the axis and its labels."),
    "axisLabel.rotate": number(
        35, -90, 90, "Rotate tick labels to fit long category names.", "°"
    ),
    "axisLabel.show": Property(False, "Toggle tick label visibility."),
    "axisLabel.hideOverlap": Property(True, "Hide labels that would collide."),
    "axisLabel.inside": Property(True, "Move tick labels into the plotting area."),
    "axisLabel.margin": number(12, 0, 50, "Space between labels and the axis.", "px"),
    "axisTick.show": Property(True, "Draw ticks at axis intervals."),
    "axisTick.inside": Property(True, "Draw ticks inside the plot."),
    "axisTick.length": number(8, 0, 30, "Adjust tick length.", "px"),
    "axisLine.show": Property(True, "Display the axis baseline."),
    "splitLine.show": Property(True, "Draw grid lines through the plotting area."),
    "splitArea.show": Property(True, "Shade alternating bands between grid lines."),
    **stroke("axisLine.lineStyle"),
    **stroke("splitLine.lineStyle"),
    "nameRotate": number(45, -90, 90, "Rotate the axis name.", "°"),
    **text_style("axisLabel"),
    **text_style("nameTextStyle"),
}
COMMON_SERIES = {
    "stack": Property(
        "total", "Give two series the same stack name to accumulate their values."
    ),
    "itemStyle.color": color("Set the fill colour of this series."),
    "itemStyle.opacity": number(0.7, 0.0, 1.0, "Control the transparency of marks."),
    "itemStyle.borderColor": color(
        "Outline the marks. Set itemStyle.borderWidth to see the edge."
    ),
    "itemStyle.borderWidth": number(
        2, 0, 12, "Change the mark outline thickness.", "px"
    ),
    "label.show": Property(True, "Write a label next to each data mark."),
    "label.position": choice(
        "Place labels relative to marks.", "top", "bottom", "inside", "left", "right"
    ),
    "label.rotate": number(30, -90, 90, "Angle mark labels.", "°"),
    "label.distance": number(
        8, 0, 40, "Adjust the gap between labels and marks.", "px"
    ),
    **text_style("label"),
    "emphasis.focus": choice(
        "Hover a mark to focus its series or just that mark.", "series", "self", "none"
    ),
    "emphasis.itemStyle.color": color(
        "Hover a mark to see its highlight colour.", "#E48645"
    ),
    "emphasis.label.show": Property(True, "Reveal a data label on hover."),
    "silent": Property(True, "Turn off pointer interactions for this series."),
    "markLine.data": Property(
        [{"type": "average"}],
        "Draw a reference line for a statistic of this series.",
        choices=("average", "median", "min", "max"),
        unit="statistic",
    ),
    "markPoint.data": Property(
        [{"type": "max"}],
        "Annotate the minimum or maximum observation in this series.",
        choices=("min", "max"),
        unit="statistic",
    ),
    "markLine.label.show": Property(
        True, "Show a label on the reference line. Add markLine.data to draw the line."
    ),
    "markPoint.symbolSize": number(
        42, 10, 90, "Resize the annotation marker created by markPoint.data.", "px"
    ),
    "label.formatter": Property(
        "{a}",
        "Use {a} for the series name or reference a field such as {@Revenue} in Monthly retail.",
    ),
    "z": number(4, 0, 20, "Draw higher values in front of overlapping series."),
}
BAR = {
    "barWidth": percent(
        48, 1, 100, "Set each bar's width as a percentage of its category band."
    ),
    "barGap": percent(
        40,
        -100,
        150,
        "Space between bars from different series in the same category. Edit the last bar series for the shared layout.",
    ),
    "barCategoryGap": percent(
        30,
        0,
        95,
        "Space between groups of bars in adjacent categories. Edit the last bar series for the shared layout.",
    ),
    "barMaxWidth": percent(
        65, 1, 100, "Limit how wide a bar can grow in its category."
    ),
    "barMinHeight": number(
        4, 0, 30, "Give very small bars a visible minimum height.", "px"
    ),
    "showBackground": Property(True, "Draw a track behind each bar."),
    "backgroundStyle.color": color(
        "Change the track colour when showBackground is enabled.", "#E2E6F4"
    ),
    "itemStyle.borderRadius": number(5, 0, 40, "Round the corners of bars.", "px"),
}
LINE = {
    "smooth": Property(True, "Curve the line between observations."),
    "connectNulls": Property(
        True, "Bridge missing observations. Try High in the Weather log."
    ),
    "step": choice(
        "Place a step between adjacent values.", "middle", "start", "end", False
    ),
    "showSymbol": Property(False, "Show or hide point markers along the line."),
    "symbol": choice(
        "Choose the point marker shape.",
        "circle",
        "emptyCircle",
        "rect",
        "roundRect",
        "triangle",
        "diamond",
        "pin",
        "arrow",
        "none",
    ),
    "symbolSize": number(9, 1, 32, "Set the marker size.", "px"),
    "areaStyle.opacity": number(
        0.25, 0.0, 1.0, "Fill the area beneath the line and set its opacity."
    ),
    "areaStyle.color": color("Choose the fill under the line."),
    "endLabel.show": Property(True, "Place a label at the end of the line."),
    **stroke("lineStyle"),
}
COMPONENTS = {
    "xAxis": {
        **AXIS,
        "position": choice("Choose the horizontal axis edge.", "bottom", "top"),
        "boundaryGap": Property(
            False, "On a category axis, toggle padding at both ends."
        ),
    },
    "yAxis": {
        **AXIS,
        "position": choice("Choose the vertical axis edge.", "left", "right"),
        "min": Property(
            0.0, "Set the lower bound of the numeric scale.", unit="number"
        ),
        "max": Property(
            100.0, "Set the upper bound of the numeric scale.", unit="number"
        ),
        "splitNumber": number(
            5, 1, 20, "Suggest how many intervals to use along the numeric scale."
        ),
        "scale": Property(
            True, "Let the value axis scale to the data range without requiring zero."
        ),
        "axisLabel.formatter": Property(
            "{value}k", "Use {value} in a text template for tick labels."
        ),
    },
    "grid": {
        edge: percent(seed, 0, 45, f"Inset the plot from the {edge} of the chart.")
        for edge, seed in (("left", 12), ("right", 8), ("top", 15), ("bottom", 18))
    },
    "tooltip": {
        "trigger": choice(
            "Inspect one mark or a whole axis position.", "axis", "item", "none"
        ),
        "axisPointer.type": choice(
            "Guide the pointer across an axis.", "shadow", "line", "cross", "none"
        ),
        "confine": Property(True, "Keep the tooltip inside the chart."),
        "backgroundColor": color("Set the tooltip panel colour.", "#FFFFFF"),
        **text_style("textStyle"),
    },
    "legend": {
        "orient": choice(
            "Arrange series names in a row or column.", "vertical", "horizontal"
        ),
        "left": choice("Align the legend horizontally.", "center", "left", "right"),
        "top": percent(3, 0, 95, "Position the legend vertically within the chart."),
        "itemGap": number(18, 0, 60, "Set the space between legend entries.", "px"),
        "selectedMode": choice(
            "Select one or multiple series by clicking legend entries.",
            "single",
            "multiple",
            False,
        ),
        **text_style("textStyle"),
    },
    "title": {
        "text": Property("Sales performance", "Set the chart title."),
        "subtext": Property("By reporting period", "Add a subtitle beneath the title."),
        "left": choice("Align the title horizontally.", "center", "left", "right"),
        **text_style("textStyle"),
        **text_style("subtextStyle"),
    },
    "dataZoom": {
        "type": choice(
            "Use a visible range slider or zoom inside the chart.", "slider", "inside"
        ),
        "start": number(
            10,
            0,
            100,
            "Start of the visible window, as a numeric percentage.",
            "% of domain",
        ),
        "end": number(
            85,
            0,
            100,
            "End of the visible window, as a numeric percentage.",
            "% of domain",
        ),
        "filterMode": choice(
            "Filter rows outside the visible window.",
            "filter",
            "weakFilter",
            "empty",
            "none",
        ),
    },
    "animation": {
        "animation": Property(False, "Toggle chart animation."),
        "animationDuration": number(
            900, 0, 3000, "Duration when marks first appear.", "ms"
        ),
        "animationDurationUpdate": number(
            800, 0, 3000, "Duration for changes to existing marks.", "ms"
        ),
        "animationEasingUpdate": choice(
            "Control the pacing of updated marks.",
            "cubicOut",
            "linear",
            "bounceOut",
            "elasticOut",
        ),
    },
}


def catalog(kind, time_axis):
    sections = {
        "series": COMMON_SERIES | (BAR if kind == "bar" else LINE),
        **COMPONENTS,
    }
    if time_axis:
        sections["xAxis"] = {
            k: v for k, v in sections["xAxis"].items() if k != "boundaryGap"
        }
    return sections


def matches(sections, query):
    words = query.lower().replace(".", " ").split()
    return [
        (section, path)
        for section, fields in sections.items()
        for path, prop in fields.items()
        if all(word in f"{section} {path} {prop.hint}".lower() for word in words)
    ]
