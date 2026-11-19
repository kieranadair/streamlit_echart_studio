"""Native dataset transforms and the tables used to inspect or fit their results."""

from dataclasses import dataclass
from operator import eq, ge, gt, le, lt, ne
from statistics import linear_regression

import pandas as pd


def axis_type(column: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(column):
        return "time"
    if pd.api.types.is_numeric_dtype(column):
        return "value"
    return "category"


@dataclass
class Transform:
    filter_field: str | None = None
    operator: str = "gte"
    value: str | float | None = None
    sort_field: str | None = None
    order: str = "desc"

    def apply(self, frame: pd.DataFrame) -> tuple[list[dict], pd.DataFrame]:
        """ECharts runs the steps. Mirror them for the preview and Python trends."""
        steps = []
        result = frame
        if self.filter_field and self.value is not None:
            column = frame[self.filter_field]
            config = {"dimension": self.filter_field, self.operator: self.value}
            threshold = self.value
            if axis_type(column) == "time":
                config["parser"] = "time"
                threshold = pd.Timestamp(self.value)
            steps.append({"type": "filter", "config": config})
            compare = {"eq": eq, "ne": ne, "gt": gt, "gte": ge, "lt": lt, "lte": le}[
                self.operator
            ]
            result = result.loc[compare(column, threshold)]
        if self.sort_field:
            ascending = self.order == "asc"
            config = {
                "dimension": self.sort_field,
                "order": self.order,
                "incomparable": "max" if ascending else "min",
            }
            if axis_type(frame[self.sort_field]) == "time":
                config["parser"] = "time"
            steps.append({"type": "sort", "config": config})
            result = result.sort_values(
                self.sort_field, ascending=ascending, kind="stable", na_position="last"
            )
        return steps, result.reset_index(drop=True) if steps else result


def trend_frame(method, window, frame, source, dimension, measure):
    """Describe the calculation alongside its result, including empty results."""
    x, y = frame[dimension], frame[measure]
    if method == "Linear fit":
        complete = x.notna() & y.notna()
        xs, ys = x[complete], y[complete]
        if xs.nunique() < 2:
            return (
                None,
                "A linear fit needs two distinct positions with observed values.",
            )
        fit = linear_regression(xs.tolist(), ys.tolist())
        ends = [float(xs.min()), float(xs.max())]
        return (
            pd.DataFrame(
                {
                    dimension: ends,
                    f"Fitted {measure}": [fit.intercept + fit.slope * v for v in ends],
                }
            ),
            f"Fitted {measure} ≈ {fit.slope:.5g} × {dimension} {fit.intercept:+.5g} · least squares over {len(xs)} complete pairs.",
        )
    # Months in the sample follow calendar order. Numeric and date fields
    # sort by their own values even if the chart was ranked by a measure.
    order = x
    if axis_type(x) == "category":
        order = x.map({value: i for i, value in enumerate(source[dimension].unique())})
    indices = order.dropna().sort_values(kind="stable").index
    average = y.loc[indices].rolling(window, min_periods=window).mean()
    if not average.notna().any():
        return (
            None,
            f"A {window}-observation average needs a full window of consecutive readings.",
        )
    return (
        pd.DataFrame(
            {dimension: x.loc[indices], f"{window}-point mean of {measure}": average}
        ).reset_index(drop=True),
        f"Ordered by {dimension}, then calculated with `{measure}.rolling({window}, min_periods={window}).mean()`.",
    )
