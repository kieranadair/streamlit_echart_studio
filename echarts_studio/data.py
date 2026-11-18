"""Small, deterministic teaching datasets. All values are illustrative."""

from dataclasses import dataclass
from datetime import date, timedelta
from math import cos, sin

import pandas as pd


@dataclass(frozen=True)
class Sample:
    dimension: str
    measures: tuple[str, ...]
    rows: tuple
    lesson: str
    time_axis: bool = False

    extra_dimensions: tuple[str, ...] = ()
    measure_column: str = "Measure"
    value_column: str = "Value"

    @property
    def columns(self):
        return (self.dimension, *self.extra_dimensions, *self.measures)

    def dataframe(self, *, heatmap=False) -> pd.DataFrame:
        frame = pd.DataFrame(self.rows, columns=self.columns)
        if self.time_axis:
            frame[self.dimension] = pd.to_datetime(frame[self.dimension])
        if heatmap:
            if self.time_axis:
                # Cartesian heatmaps use category labels on both axes.
                frame[self.dimension] = frame[self.dimension].dt.strftime("%Y-%m-%d")
            cells = (
                frame.melt(
                    id_vars=[self.dimension, *self.extra_dimensions],
                    value_vars=self.measures,
                    var_name=self.measure_column,
                    value_name=self.value_column,
                    ignore_index=False,
                )
                .sort_index(kind="stable")
                .reset_index(drop=True)
            )
            frame = cells[
                [
                    self.dimension,
                    self.measure_column,
                    self.value_column,
                    *self.extra_dimensions,
                ]
            ]
        return frame


SAMPLES = {
    "Monthly retail": Sample(
        "Month",
        ("Revenue", "Target"),
        tuple(
            zip(
                [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ],
                (42, 48, 45, 58, 62, 56, 68, 72, 65, 79, 88, 98),
                (45, 46, 49, 52, 56, 60, 64, 66, 70, 75, 80, 92),
                strict=True,
            )
        ),
        "Monthly revenue and sales targets, in thousands of dollars.",
    ),
    "Regional channels": Sample(
        "Region",
        ("Stores", "Online", "Wholesale"),
        (
            ("Pacific Northwest", 61, 48, 20),
            ("Southern Highlands", 52, 36, 28),
            ("Central Valley", 67, 50, 21),
            ("Northern Coast", 43, 39, 26),
            ("Eastern Seaboard", 81, 57, 32),
            ("Western Plains", 38, 31, 18),
        ),
        "Regional sales by channel, in thousands of dollars.",
        measure_column="Channel",
        value_column="Sales",
    ),
    "Weather log": Sample(
        "Date",
        ("High", "Low"),
        tuple(
            (
                (date(2025, 4, 1) + timedelta(days=i)).isoformat(),
                i + 1,
                None if 19 <= i <= 22 else round(17 + i * 0.12 + 3 * sin(i / 3), 1),
                round(9 + i * 0.08 + 2 * cos(i / 4), 1),
            )
            for i in range(60)
        ),
        "Daily temperatures in °C. Four consecutive high readings are missing.",
        time_axis=True,
        extra_dimensions=("Day",),
        measure_column="Reading",
        value_column="Temperature",
    ),
}


# Each example opens with data that illustrates its bindings. Learners can
# still switch datasets and keep an independent document for each combination.
EXAMPLE_DATASETS = {
    "Bar chart": "Monthly retail",
    "Stacked bars": "Regional channels",
    "Area chart": "Monthly retail",
    "Scatter plot": "Regional channels",
    "Bubble plot": "Regional channels",
    "Heatmap": "Regional channels",
}
