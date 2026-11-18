"""Build the native option from data bindings and explicitly edited properties."""

from dataclasses import dataclass, field
from pprint import pformat
from typing import Any

import pandas as pd

from .data import Sample
from .schema import COMMON_SERIES, OPTIONAL_BRANCHES


@dataclass
class Series:
    kind: str = "bar"
    x_override: str | None = None
    common: dict = field(default_factory=dict)
    bar: dict = field(default_factory=dict)
    line: dict = field(default_factory=dict)

    def settings(self, path):
        return self.common if path in COMMON_SERIES else getattr(self, self.kind)


@dataclass
class Document:
    measures: list[str]
    shared_x: str
    series: dict[str, Series]
    axes: dict[str, dict]
    components: dict[str, dict]
    enabled: set[str]

    @classmethod
    def for_sample(cls, sample: Sample):
        return cls(
            measures=[sample.measures[0]],
            shared_x=sample.dimension,
            series={m: Series() for m in sample.measures},
            axes={column: {} for column in sample.columns},
            components={group: {} for group in ("yAxis", *OPTIONAL_BRANCHES)},
            enabled={"tooltip"},
        )

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
            "yAxis": {"type": "value", **nested(self.components["yAxis"])},
            "series": [],
        }
        for measure in self.measures:
            series = self.series[measure]
            x_field = self.x_for(measure)
            entry = {
                "name": measure,
                "type": series.kind,
                "encode": {"x": x_field, "y": measure},
            }
            if len(fields) > 1:
                entry["xAxisIndex"] = fields.index(x_field)
            entry.update(nested(series.common | getattr(series, series.kind)))
            option["series"].append(entry)
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
