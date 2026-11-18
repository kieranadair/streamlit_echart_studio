"""Small, deterministic teaching datasets. All values are illustrative."""

from dataclasses import dataclass
from datetime import date, timedelta
from math import cos, sin


@dataclass(frozen=True)
class Sample:
    dimension: str
    measures: tuple[str, ...]
    rows: tuple
    lesson: str
    time_axis: bool = False

    def records(self):
        columns = (self.dimension, *self.measures)
        return [dict(zip(columns, row, strict=True)) for row in self.rows]


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
    ),
    "Weather log": Sample(
        "Date",
        ("High", "Low"),
        tuple(
            (
                (date(2025, 4, 1) + timedelta(days=i)).isoformat(),
                None if 19 <= i <= 22 else round(17 + i * 0.12 + 3 * sin(i / 3), 1),
                round(9 + i * 0.08 + 2 * cos(i / 4), 1),
            )
            for i in range(60)
        ),
        "Daily temperatures in °C. Four consecutive high readings are missing.",
        True,
    ),
}
