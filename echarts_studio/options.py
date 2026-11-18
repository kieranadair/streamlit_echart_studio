"""Editor state lives independently of widget lifetimes and of the rendered option."""

from dataclasses import dataclass, field

from .data import Sample
from .schema import COMMON_SERIES


@dataclass
class Series:
    kind: str = "bar"
    common: dict = field(default_factory=dict)
    bar: dict = field(default_factory=dict)
    line: dict = field(default_factory=dict)

    def settings(self, path):
        return self.common if path in COMMON_SERIES else getattr(self, self.kind)


@dataclass
class Document:
    measures: list
    series: dict
    components: dict
    enabled: set

    @classmethod
    def for_sample(cls, sample):
        components = {
            key: {}
            for key in (
                "grid",
                "xAxis",
                "yAxis",
                "tooltip",
                "legend",
                "title",
                "dataZoom",
                "animation",
            )
        }
        components["tooltip"]["trigger"] = "axis"
        palette = ("#425BBD", "#C26C33", "#318478")
        series = {
            m: Series(common={"itemStyle.color": palette[i]})
            for i, m in enumerate(sample.measures)
        }
        return cls(
            [sample.measures[0]], series, components, {"xAxis", "yAxis", "tooltip"}
        )

    def build(self, sample: Sample):
        option = {}
        for group, values in self.components.items():
            if group not in self.enabled:
                continue
            if group == "animation":
                option.update(nested(values))
                continue
            defaults = {}
            if group == "xAxis":
                defaults["type"] = "time" if sample.time_axis else "category"
            elif group == "yAxis":
                defaults["type"] = "value"
            option[group] = nested(defaults | values)
        option["series"] = []
        for measure in self.measures:
            series = self.series[measure]
            style = nested(series.common | getattr(series, series.kind))
            option["series"].append(
                {
                    "name": measure,
                    "type": series.kind,
                    "encode": {"x": sample.dimension, "y": measure},
                    **style,
                }
            )
        option["dataset"] = {"source": sample.records()}
        return option


def nested(values):
    tree = {}
    for path, value in values.items():
        parent = tree
        *ancestors, leaf = path.split(".")
        for name in ancestors:
            parent = parent.setdefault(name, {})
        parent[leaf] = value
    return tree
