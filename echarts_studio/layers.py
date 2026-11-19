"""Data-bound annotations, colour thresholds and responsive canvas layouts."""

from dataclasses import dataclass, field
from uuid import uuid4

import pandas as pd


def row_id():
    return uuid4().hex[:12]


def coordinate(value):
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value.item() if hasattr(value, "item") else value


@dataclass
class Reference:
    kind: str
    column: str
    start: str | float = 0
    end: str | float = 0
    name: str = ""
    statistic: str = "average"
    colour: str = "#69758a"
    width: int = 2
    dash: str = "dashed"
    opacity: float = 0.15
    axis_when_shared: str = "yAxis"
    uid: str = field(default_factory=row_id)

    def axis(self, x, y):
        if x == y:
            return self.axis_when_shared
        return "yAxis" if self.column == y else "xAxis"

    def option(self, x, y, axes):
        if self.column not in (x, y):
            return None
        axis = self.axis(x, y)
        start, end = self.start, self.end
        scale, positions = axes[axis]
        if self.kind == "Statistic" and scale != "value":
            return None
        if positions is not None:
            # ECharts treats numeric coordinates on an ordinal scale as indices.
            # Index into the displayed categories, which can change after a sort.
            try:
                start = int(positions.get_loc(start))
                if self.kind == "Band":
                    end = int(positions.get_loc(end))
            except KeyError:
                return None
        show_value = self.kind == "Statistic" or (
            self.kind == "Fixed" and isinstance(self.start, (int, float))
        )
        formatter = "{b} · {c}" if show_value and scale != "category" else "{b}"
        attrs = (
            {"name": self.name, "label": {"formatter": formatter}} if self.name else {}
        )
        if self.kind == "Band":
            return [
                {
                    **attrs,
                    axis: start,
                    "itemStyle": {"color": self.colour, "opacity": self.opacity},
                },
                {axis: end},
            ]
        position = (
            {"type": self.statistic, "valueDim": self.column}
            if self.kind == "Statistic"
            else {axis: start}
        )
        return {
            **attrs,
            **position,
            "lineStyle": {"color": self.colour, "width": self.width, "type": self.dash},
        }


@dataclass
class ColourBand:
    label: str
    colour: str
    upper: float | None = None
    uid: str = field(default_factory=row_id)


def default_bands(low, high):
    step = (high - low) / 3
    return [
        ColourBand("Low", "#dfeef7", round(low + step, 3)),
        ColourBand("Middle", "#79a7c9", round(low + 2 * step, 3)),
        ColourBand("High", "#204995"),
    ]


def colour_pieces(bands):
    pieces = []
    lower = None
    for band in bands:
        piece = {"color": band.colour}
        if band.label:
            piece["label"] = band.label
        if lower is not None:
            piece["gt"] = lower
        if band.upper is not None:
            piece["lte"] = band.upper
        pieces.append(piece)
        lower = band.upper
    return pieces


LEGEND_PLACEMENTS = {
    "Bottom": {"orient": "horizontal", "left": "center", "top": "bottom"},
    "Top": {"orient": "horizontal", "left": "center", "top": "top"},
    "Right": {"orient": "vertical", "left": "right", "top": "middle"},
    "Left": {"orient": "vertical", "left": "left", "top": "middle"},
}


@dataclass
class MediaRule:
    condition: str = "maxWidth"
    limit: float = 500
    placement: str = "Bottom"
    grid_edge: str | None = None
    inset: int = 10
    uid: str = field(default_factory=row_id)


def responsive_option(option, rules):
    if not rules:
        return option
    legend = option.get("legend", {})
    base_grid = option.get("grid", {})
    grids = base_grid if isinstance(base_grid, list) else [base_grid]
    edges = {rule.grid_edge for rule in rules if rule.grid_edge}
    defaults = {"left": "15%", "right": "10%"}

    def grid_option(layouts):
        return layouts if isinstance(base_grid, list) else layouts[0]

    media = []
    for rule in rules:
        layout = {"legend": {"show": True, **LEGEND_PLACEMENTS[rule.placement]}}
        if rule.grid_edge:
            layout["grid"] = grid_option(
                [{rule.grid_edge: f"{rule.inset}%"} for _ in grids]
            )
        media.append({"query": {rule.condition: rule.limit}, "option": layout})

    normal = {
        "show": "legend" in option,
        "orient": "horizontal",
        "left": "center",
        "top": None,
        "bottom": 15,
    }
    normal.update({k: v for k, v in legend.items() if k in normal})
    baseline = {"legend": normal}
    if edges:
        baseline["grid"] = grid_option(
            [
                {edge: grid.get(edge, defaults[edge]) for edge in sorted(edges)}
                for grid in grids
            ]
        )
    if len(rules) == 1:
        media.append({"option": baseline})
    else:
        # ECharts merges matching options on resize. Start each combination
        # from the base layout so an expired inset doesn't carry into another rule.
        media.insert(0, {"query": {}, "option": baseline})
    return {"baseOption": option, "media": media}


def panel_grids(settings, count, canvas_height, gap):
    """Divide the space between the configured outer insets into equal panels."""

    def as_percent(value):
        if isinstance(value, str):
            return float(value.removesuffix("%"))
        return 100 * value / canvas_height

    top = as_percent(settings.get("top", 65))
    bottom = as_percent(settings.get("bottom", 80))
    available = max(1, 100 - top - bottom)
    gap = min(gap, available / (2 * count))
    height = (available - (count - 1) * gap) / count
    shared = {k: v for k, v in settings.items() if k not in ("top", "bottom")}
    return [
        {
            **shared,
            "top": f"{top + i * (height + gap):.4g}%",
            "height": f"{height:.4g}%",
        }
        for i in range(count)
    ]
