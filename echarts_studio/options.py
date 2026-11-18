"""Build the native option from data bindings and explicitly edited properties."""

from dataclasses import dataclass, field
from pprint import pformat
from typing import Any

import pandas as pd

from .data import Sample
from .schema import OPTIONAL_BRANCHES, SERIES_FIELDS, SERIES_SPECIFIC


@dataclass
class VisualMapping:
    dimension: str | None = None
    domains: dict[str, tuple[float, float]] = field(default_factory=dict)
    sizes: tuple[int, int] = (8, 36)
    colours: tuple[str, str] = ("#e6effa", "#204995")
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

    def option(self, frame, column, index, heatmap):
        limits = self.domains.get(column) or self.data_range(frame[column])
        channel = (
            {"color": list(self.colours)}
            if heatmap
            else {"symbolSize": list(self.sizes)}
        )
        return {
            "type": "continuous",
            "seriesIndex": index,
            "dimension": int(frame.columns.get_loc(column)),
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
            components={group: {} for group in ("yAxis", *OPTIONAL_BRANCHES)},
            enabled={"tooltip"},
            item_name=sample.dimension,
            category_y=sample.dimension if heatmap else None,
        )
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
        elif example in ("Scatter plot", "Bubble plot"):
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
        return doc

    def x_for(self, measure):
        return self.series[measure].x_override or self.shared_x

    def x_fields(self):
        # Reuse an axis when two series use the same dimension.
        return list(dict.fromkeys(self.x_for(m) for m in self.measures)) or [
            self.shared_x
        ]

    def build(self, frame: pd.DataFrame):
        fields = self.x_fields()
        x_axes = []
        used_edges = {"bottom": 0, "top": 0}
        for column in fields:
            axis: dict[str, Any] = {
                "type": axis_type(frame[column]),
                **nested(self.axes[column]),
            }
            # ECharts assigns the first free bottom edge, then the top edge.
            edge = axis.get("position", "top" if used_edges["bottom"] else "bottom")
            if used_edges[edge]:
                axis["offset"] = 40 * used_edges[edge]
            used_edges[edge] += 1
            x_axes.append(axis)

        option = {
            "dataset": {"source": frame},
            "xAxis": x_axes[0] if len(x_axes) == 1 else x_axes,
            "yAxis": {
                "type": "category" if self.category_y else "value",
                **nested(self.components["yAxis"]),
            },
            "series": [],
        }
        visual_maps = []
        for index, measure in enumerate(self.measures):
            series = self.series[measure]
            x_field = self.x_for(measure)
            encode: dict[str, Any] = {"x": x_field, "y": self.category_y or measure}
            mapped_column = None
            if self.category_y:
                encode["value"] = measure
                mapped_column = measure
            elif series.kind == "scatter":
                mapped_column = series.mapping.dimension
                dimensions = [self.item_name, x_field, measure]
                if mapped_column:
                    dimensions.append(mapped_column)
                encode.update(
                    itemName=self.item_name, tooltip=list(dict.fromkeys(dimensions))
                )
            if mapped_column is not None:
                visual_maps.append(
                    series.mapping.option(
                        frame, mapped_column, index, self.category_y is not None
                    )
                )
            entry = {
                "name": measure,
                "type": series.kind,
                "encode": encode,
            }
            if len(fields) > 1:
                entry["xAxisIndex"] = fields.index(x_field)
            entry.update(series.style())
            option["series"].append(entry)
        if visual_maps:
            option["visualMap"] = (
                visual_maps[0] if len(visual_maps) == 1 else visual_maps
            )
        for group in OPTIONAL_BRANCHES:
            if group not in self.enabled:
                continue
            settings = nested(self.components[group])
            if group == "animation":
                option.update(settings)
            else:
                option[group] = settings
        return option


def axis_type(column: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(column):
        return "time"
    if pd.api.types.is_numeric_dtype(column):
        return "value"
    return "category"


def option_code(option):
    """Show executable Python with a reference to the same DataFrame as the chart."""

    class FrameName:
        def __repr__(self):
            return "df"

    display = {**option, "dataset": {**option["dataset"], "source": FrameName()}}
    return "option = " + pformat(display, sort_dicts=False, width=75)


def nested(values):
    tree = {}
    for path, value in values.items():
        parent = tree
        *ancestors, leaf = path.split(".")
        for name in ancestors:
            parent = parent.setdefault(name, {})
        parent[leaf] = value
    return tree
