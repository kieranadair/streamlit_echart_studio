"""Build the native option from data bindings and explicitly edited properties."""

from dataclasses import dataclass, field
from pprint import pformat
from typing import Any

import pandas as pd

from .data import Sample
from .datasets import Transform, axis_type, trend_frame
from .layers import (
    ColourBand,
    MediaRule,
    Reference,
    colour_pieces,
    coordinate,
    default_bands,
    panel_grids,
    responsive_option,
)
from .schema import (
    COMPONENTS,
    OPTIONAL_BRANCHES,
    SERIES_FIELDS,
    SERIES_SPECIFIC,
    axis_properties,
)


@dataclass
class VisualMapping:
    dimension: str | None = None
    domains: dict[str, tuple[float, float]] = field(default_factory=dict)
    sizes: tuple[int, int] = (8, 36)
    colours: tuple[str, str] = ("#e6effa", "#204995")
    kind: str = "continuous"
    bands: dict[str, list[ColourBand]] = field(default_factory=dict)
    settings: dict = field(
        default_factory=lambda: {
            "show": False,
            "orient": "horizontal",
            "left": "center",
        }
    )

    @staticmethod
    def data_range(column: pd.Series) -> tuple[float, float]:
        values = column.dropna()
        if values.empty:
            return (0.0, 1.0)
        low, high = float(values.min()), float(values.max())
        return (low, high if high > low else low + 1.0)

    def bands_for(self, frame, column):
        if column not in self.bands:
            self.bands[column] = default_bands(*self.data_range(frame[column]))
        return self.bands[column]

    def option(self, frame, column, index, heatmap):
        target = {"seriesIndex": index, "dimension": int(frame.columns.get_loc(column))}
        if heatmap and self.kind == "piecewise":
            return {
                "type": "piecewise",
                **target,
                "pieces": colour_pieces(self.bands_for(frame, column)),
                **{k: v for k, v in self.settings.items() if k != "calculable"},
            }
        limits = self.domains.get(column) or self.data_range(frame[column])
        channel = (
            {"color": list(self.colours)}
            if heatmap
            else {"symbolSize": list(self.sizes)}
        )
        return {
            "type": "continuous",
            **target,
            "min": limits[0],
            "max": limits[1],
            "inRange": channel,
            **self.settings,
        }


@dataclass
class Series:
    kind: str = "bar"
    x_override: str | None = None
    common: dict = field(default_factory=dict)
    bar: dict = field(default_factory=dict)
    line: dict = field(default_factory=dict)
    scatter: dict = field(default_factory=dict)
    heatmap: dict = field(default_factory=dict)
    mapping: VisualMapping = field(default_factory=VisualMapping)
    tooltip_fields: list[str] | None = None
    references: list[Reference] = field(default_factory=list)
    trend: str = "None"
    window: int = 3

    def settings(self, path):
        return (
            getattr(self, self.kind)
            if path in SERIES_SPECIFIC[self.kind]
            else self.common
        )

    def style(self):
        # A shared edit (e.g. stack) can be meaningful for only some types.
        flat = {}
        for path in SERIES_FIELDS[self.kind]:
            values = self.settings(path)
            if path in values:
                flat[path] = values[path]
        return nested(flat)

    def encode(self, x, y, item_name, cell_value=None):
        encode = {"x": x, "y": y}
        if cell_value:
            encode["value"] = cell_value
        if self.kind == "scatter":
            fields = [item_name, x, y]
            if self.mapping.dimension:
                fields.append(self.mapping.dimension)
            encode.update(itemName=item_name, tooltip=list(dict.fromkeys(fields)))
        if self.tooltip_fields is not None:
            encode["tooltip"] = self.tooltip_fields
        return encode

    def add_references(self, entry, x, y, axes):
        for reference in self.references:
            item = reference.option(x, y, axes)
            if item is not None:
                branch = "markArea" if reference.kind == "Band" else "markLine"
                settings = entry.setdefault(branch, {})
                settings["data"] = [*settings.get("data", []), item]


@dataclass
class CompiledChart:
    option: dict
    plotted: pd.DataFrame
    trends: list[tuple[str, pd.DataFrame]]
    messages: list[str]


@dataclass
class Document:
    measures: list[str]
    shared_x: str
    series: dict[str, Series]
    axes: dict[str, dict]
    components: dict[str, dict]
    enabled: set[str]
    item_name: str
    category_y: str | None = None
    horizontal: bool = False
    horizontal_axes: dict = field(default_factory=dict)
    horizontal_values: dict = field(default_factory=dict)
    transform: Transform = field(default_factory=Transform)
    panels: bool = False
    panel_gap: int = 8
    link_pointers: bool = False
    media_rules: list[MediaRule] = field(default_factory=lambda: [MediaRule()])
    note_corner: str = "Bottom right"
    note_inset: int = 2
    brush_tools: list[str] = field(default_factory=lambda: ["rect", "polygon"])
    preview_width: int | None = None
    preview_height: int = 560

    @classmethod
    def for_sample(cls, sample: Sample, example="Bar chart", frame=None):
        heatmap = example == "Heatmap"
        if frame is None:
            frame = sample.dataframe(heatmap=heatmap)
        numeric = (
            frame.select_dtypes("number").columns.tolist()
            if heatmap
            else list(sample.measures)
        )
        first_measure = sample.value_column if heatmap else sample.measures[0]
        doc = cls(
            measures=[first_measure],
            shared_x=sample.measure_column if heatmap else sample.dimension,
            series={m: Series(kind="heatmap" if heatmap else "bar") for m in numeric},
            axes={column: {} for column in frame.columns},
            components={group: {} for group in ("yAxis", *COMPONENTS)},
            enabled={"tooltip"},
            item_name=sample.dimension,
            category_y=sample.dimension if heatmap else None,
        )
        doc.components["toolbox"] = {"feature.dataZoom": {}, "feature.restore": {}}
        doc.components["graphic"]["style.text"] = "Source · ECharts Studio sample data"
        doc.components["brush"]["outOfBrush.opacity"] = 0.25
        if heatmap:
            for column, series in doc.series.items():
                series.mapping.settings.pop("show")
                # The native heatmap label reads the third source dimension.
                if frame.columns.get_loc(column) != 2:
                    series.common["label.formatter"] = "{@" + column + "}"
                if len(frame) <= 24:
                    series.common["label.show"] = True
        elif example == "Stacked bars":
            doc.measures = list(sample.measures)
            for series in doc.series.values():
                series.common["stack"] = "total"
            doc.enabled.add("legend")
        elif example == "Area chart":
            series = doc.series[first_measure]
            series.kind = "line"
            series.line["areaStyle.opacity"] = 0.35
        elif example in ("Scatter plot", "Bubble plot", "Linear fit"):
            doc.shared_x, measure = sample.measures[:2]
            doc.measures = [measure]
            series = doc.series[measure]
            series.kind = "scatter"
            if example == "Bubble plot":
                other = [
                    c
                    for c in frame.select_dtypes("number")
                    if c not in (doc.shared_x, measure)
                ]
                series.mapping.dimension = other[0] if other else measure
                series.mapping.settings.pop("show")
            elif example == "Linear fit":
                series.trend = "Linear fit"
        elif example == "Rank the regions":
            doc.horizontal = True
            doc.horizontal_axes[sample.dimension] = {"inverse": True}
            if sample.time_axis:
                doc.horizontal_axes[sample.dimension]["type"] = "category"
            doc.transform.sort_field = first_measure
        elif example == "Moving average":
            series = doc.series[first_measure]
            series.kind = "line"
            series.trend = "Moving average"
            if sample.dimension == "Region":
                doc.shared_x = sample.measures[1]
        elif example == "Benchmarks and bands":
            is_retail = sample.dimension == "Month"
            levels = frame[first_measure].dropna()
            benchmark = 60 if is_retail else float(levels.median())
            dates = frame[sample.dimension]
            doc.series[first_measure].references = [
                Reference("Fixed", first_measure, benchmark, name="Benchmark"),
                Reference("Statistic", first_measure, name="Mean", colour="#c0572b"),
                Reference(
                    "Band",
                    sample.dimension,
                    coordinate(dates.iloc[len(dates) // 4]),
                    coordinate(dates.iloc[len(dates) // 2 - 1]),
                    name="Q2" if is_retail else "Study interval",
                    colour="#4777ac",
                ),
            ]
        elif example in ("Linked panels", "Responsive layout"):
            doc.measures = list(sample.measures[:2])
            doc.series[doc.measures[1]].kind = "line"
            doc.enabled.update(("grid", "legend"))
            if example == "Linked panels":
                doc.panels = doc.link_pointers = True
                doc.components["tooltip"]["trigger"] = "axis"
            else:
                doc.enabled.add("media")
                doc.components["legend"].update(
                    orient="vertical", left="right", top="12%"
                )
                doc.components["grid"]["right"] = "24%"
                doc.media_rules = [MediaRule(grid_edge="right", inset=8)]
        return doc

    def x_for(self, measure):
        return self.series[measure].x_override or self.shared_x

    def x_fields(self):
        # Reuse an axis when two series use the same dimension.
        return list(dict.fromkeys(self.x_for(m) for m in self.measures)) or [
            self.shared_x
        ]

    @property
    def dimension_axis(self):
        return "yAxis" if self.horizontal else "xAxis"

    def bindings(self, measure):
        dimension = self.x_for(measure)
        if self.horizontal:
            return measure, dimension
        return dimension, self.category_y or measure

    def axis_settings(self, branch, dimension):
        if branch == self.dimension_axis:
            return (
                self.horizontal_axes.setdefault(dimension, {})
                if self.horizontal
                else self.axes[dimension]
            )
        return self.horizontal_values if self.horizontal else self.components["yAxis"]

    def inferred_axis_type(self, branch, dimension, frame):
        if branch == self.dimension_axis:
            return axis_type(frame[dimension])
        return "category" if self.category_y else "value"

    def axis_kind(self, branch, dimension, frame):
        return self.axis_settings(branch, dimension).get(
            "type", self.inferred_axis_type(branch, dimension, frame)
        )

    def trend_methods(self, measure, frame):
        methods = ["None"]
        dimension = self.x_for(measure)
        value_axis = "xAxis" if self.horizontal else "yAxis"
        if self.axis_kind(value_axis, dimension, frame) != "value":
            return methods
        scale = self.axis_kind(self.dimension_axis, dimension, frame)
        if scale == "value":
            methods.append("Linear fit")
        if scale in ("value", "time") or dimension == "Month":
            methods.append("Moving average")
        return methods

    def _axis(self, branch, dimension, frame):
        kind = self.axis_kind(branch, dimension, frame)
        allowed = axis_properties(kind)
        values = self.axis_settings(branch, dimension)
        style = {k: v for k, v in values.items() if k in allowed or k == "position"}
        return {"type": kind, **nested(style)}

    def reference_axes(self, measure, frame, plotted):
        dimension = self.x_for(measure)
        axes = {}
        for axis, column in zip(
            ("xAxis", "yAxis"), self.bindings(measure), strict=True
        ):
            scale = self.axis_kind(axis, dimension, frame)
            positions = None
            if scale == "category" and axis_type(frame[column]) != "category":
                separate = axis == self.dimension_axis or (
                    self.panels and "grid" in self.enabled
                )
                fields = [column] if separate else self.measures
                values = pd.concat([plotted[c] for c in fields], ignore_index=True)
                positions = pd.Index(values.drop_duplicates())
            axes[axis] = (scale, positions)
        return axes

    def cartesian(self, frame):
        """Lay out the physical axes once and share their indices with overlays."""
        dim_axis = self.dimension_axis
        value_axis = "xAxis" if self.horizontal else "yAxis"
        settings = nested(self.components["grid"]) if "grid" in self.enabled else {}
        if "grid" in self.enabled and self.panels and len(self.measures) > 1:
            grids = panel_grids(
                settings, len(self.measures), self.preview_height, self.panel_gap
            )
            axes: dict[str, Any] = {"xAxis": [], "yAxis": [], "grid": grids}
            indices = {}
            by_dimension = {}
            for i, measure in enumerate(self.measures):
                dimension = self.x_for(measure)
                for branch in ("xAxis", "yAxis"):
                    panel_axis = {
                        **self._axis(branch, dimension, frame),
                        "gridIndex": i,
                    }
                    if branch == value_axis:
                        panel_axis.setdefault("name", measure)
                    axes[branch].append(panel_axis)
                indices[measure] = {"xAxisIndex": i, "yAxisIndex": i}
                by_dimension.setdefault(dimension, []).append(i)
            links = [
                {dim_axis + "Index": group}
                for group in by_dimension.values()
                if len(group) > 1
            ]
            if self.link_pointers and links:
                axes["axisPointer"] = {"show": True, "link": links}
            return axes, indices

        fields = self.x_fields()
        first, second = ("left", "right") if self.horizontal else ("bottom", "top")
        used = {first: 0, second: 0}
        dim_axes = []
        for column in fields:
            axis = self._axis(dim_axis, column, frame)
            edge = axis.get("position", second if used[first] else first)
            if used[edge]:
                axis["offset"] = 40 * used[edge]
            used[edge] += 1
            dim_axes.append(axis)
        axes = {
            dim_axis: dim_axes[0] if len(fields) == 1 else dim_axes,
            value_axis: self._axis(value_axis, fields[0], frame),
        }
        if "grid" in self.enabled:
            axes["grid"] = settings
        indices = {
            m: {dim_axis + "Index": fields.index(self.x_for(m))}
            if len(fields) > 1
            else {}
            for m in self.measures
        }
        return axes, indices

    def compile(self, frame: pd.DataFrame) -> CompiledChart:
        steps, plotted = self.transform.apply(frame)
        datasets: list[dict] = [{"source": frame}]
        if steps:
            datasets.append(
                {
                    "fromDatasetIndex": 0,
                    "transform": steps[0] if len(steps) == 1 else steps,
                }
            )
        axes, indices = self.cartesian(frame)
        entries, overlays, maps, trends, messages = [], [], [], [], []
        for index, measure in enumerate(self.measures):
            series = self.series[measure]
            x, y = self.bindings(measure)
            cell = measure if self.category_y else None
            mapped = cell or (
                series.mapping.dimension if series.kind == "scatter" else None
            )
            entry = {
                "name": measure,
                "type": series.kind,
                "encode": series.encode(x, y, self.item_name, cell),
                **indices[measure],
                **series.style(),
            }
            if steps:
                entry["datasetIndex"] = 1
            if mapped is not None:
                maps.append(
                    series.mapping.option(frame, mapped, index, cell is not None)
                )
            if series.references:
                series.add_references(
                    entry, x, y, self.reference_axes(measure, frame, plotted)
                )
            entries.append(entry)
            if series.trend == "None" or self.category_y:
                continue
            if series.trend not in self.trend_methods(measure, frame):
                requirement = (
                    "a numeric dimension on a value scale"
                    if series.trend == "Linear fit"
                    else "a numeric or time scale, or the Month field"
                )
                messages.append(
                    f"{measure} · {series.trend} needs {requirement} and a value scale for the measure."
                )
                continue
            dimension = self.x_for(measure)
            derived, explanation = trend_frame(
                series.trend, series.window, plotted, frame, dimension, measure
            )
            if derived is None:
                messages.append(f"{measure} · {explanation}")
                continue
            name = derived.columns[-1]
            trends.append((explanation, derived))
            tx, ty = (name, dimension) if self.horizontal else (dimension, name)
            overlays.append(
                {
                    "name": name,
                    "type": "line",
                    "datasetIndex": len(datasets),
                    "encode": {"x": tx, "y": ty},
                    **indices[measure],
                    "showSymbol": False,
                    "lineStyle": {"type": "dashed"},
                }
            )
            datasets.append({"source": derived})

        option: dict[str, Any] = {
            "dataset": datasets[0] if len(datasets) == 1 else datasets,
            **axes,
            "series": entries + overlays,
        }
        if maps:
            option["visualMap"] = maps[0] if len(maps) == 1 else maps
        option.update(nested(self.components["Chart"]))
        for group in OPTIONAL_BRANCHES:
            if group not in self.enabled or group in ("grid", "media"):
                continue
            settings = nested(self.components[group])
            if group == "animation":
                option.update(settings)
            elif group == "graphic":
                if settings.get("style", {}).get("text"):
                    vertical, horizontal = self.note_corner.lower().split()
                    inset = f"{self.note_inset}%"
                    option[group] = {
                        "elements": [
                            {
                                "type": "text",
                                "silent": True,
                                vertical: inset,
                                horizontal: inset,
                                **settings,
                            }
                        ]
                    }
            elif group == "aria":
                option[group] = {"enabled": True, **settings}
            elif group == "brush":
                targets = [
                    i for i, s in enumerate(entries) if s["type"] in ("bar", "scatter")
                ]
                if targets and self.brush_tools:
                    option[group] = {
                        "toolbox": [*self.brush_tools, "clear"],
                        "xAxisIndex": "all",
                        "seriesIndex": targets,
                        **settings,
                    }
            else:
                option[group] = settings
        if "media" in self.enabled:
            option = responsive_option(option, self.media_rules)
        return CompiledChart(option, plotted, trends, messages)

    def build(self, frame: pd.DataFrame):
        return self.compile(frame).option


def option_code(option):
    """Preserve wrappers and dataset indices, naming each actual DataFrame."""

    class FrameName:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return self.name

    names = {}

    def display(value):
        if isinstance(value, pd.DataFrame):
            return names.setdefault(
                id(value), FrameName("df" if not names else f"trend_df_{len(names)}")
            )
        if isinstance(value, dict):
            return {key: display(item) for key, item in value.items()}
        if isinstance(value, list):
            return [display(item) for item in value]
        return value

    return "option = " + pformat(display(option), sort_dicts=False, width=75)


def nested(values):
    tree = {}
    for path, value in values.items():
        parent = tree
        *ancestors, leaf = path.split(".")
        for name in ancestors:
            parent = parent.setdefault(name, {})
        parent[leaf] = value
    return tree
