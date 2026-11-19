import json

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from echarts_studio.data import EXAMPLE_DATASETS, SAMPLES
from echarts_studio.datasets import Transform
from echarts_studio.layers import MediaRule, Reference
from echarts_studio.options import Document, option_code


def render(app):
    assert not app.exception
    assert not app.warning
    return json.loads(app.get("echarts_chart")[0].proto.spec)


def branch(app, name):
    app.session_state["option_branches"] = name
    app.run()


def start(example):
    app = AppTest.from_file("../app.py").run()
    return app.selectbox(key="example").select(example).run()


@pytest.mark.parametrize("example", list(EXAMPLE_DATASETS))
def test_examples_use_the_real_sources_for_every_dataset(example):
    for sample in SAMPLES.values():
        source = sample.dataframe(heatmap=example == "Heatmap")
        doc = Document.for_sample(sample, example, source)
        result = doc.compile(source)
        base = result.option.get("baseOption", result.option)
        datasets = (
            base["dataset"] if isinstance(base["dataset"], list) else [base["dataset"]]
        )
        assert datasets[0]["source"] is source
        namespace = {"df": source}
        for i, (_, frame) in enumerate(result.trends, 1):
            namespace[f"trend_df_{i}"] = frame
        exec(option_code(result.option), namespace)  # noqa: S102 -- exercise the option shown to the learner
        assert namespace["option"] == result.option
        for series in base["series"]:
            assert "data" not in series
            assert series.get("datasetIndex", 0) < len(datasets)


@pytest.mark.parametrize(
    ("operator", "expected"),
    [
        ("gte", [81, 67, 61]),
        ("gt", [81, 67]),
        ("lte", [61, 52, 43, 38]),
        ("lt", [52, 43, 38]),
        ("eq", [61]),
    ],
)
def test_ranked_native_filter_and_preview_agree(operator, expected):
    source = SAMPLES["Regional channels"].dataframe()
    transform = Transform("Stores", operator, 61, "Stores", "desc")
    steps, plotted = transform.apply(source)
    assert plotted["Stores"].tolist() == expected
    assert steps[0] == {
        "type": "filter",
        "config": {"dimension": "Stores", operator: 61},
    }
    assert steps[1]["config"] == {
        "dimension": "Stores",
        "order": "desc",
        "incomparable": "min",
    }


def test_date_filter_sort_and_missing_observations():
    df = SAMPLES["Weather log"].dataframe()
    steps, plotted = Transform("Date", "gte", "2025-04-20", "High", "asc").apply(df)
    assert steps[0]["config"]["parser"] == "time"
    assert plotted["Date"].min() == pd.Timestamp("2025-04-20")
    assert plotted["High"].tail(4).isna().all()
    _, only_online = Transform("Region", "eq", "Central Valley").apply(
        SAMPLES["Regional channels"].dataframe()
    )
    assert only_online["Online"].tolist() == [50]


def test_filtered_trend_indices_order_and_degenerate_fit():
    sample = SAMPLES["Regional channels"]
    df = sample.dataframe()
    doc = Document.for_sample(sample, "Linear fit")
    doc.series["Online"].mapping.dimension = "Wholesale"
    doc.transform = Transform("Stores", "gte", 60, "Online", "desc")
    result = doc.compile(df)
    base, fit = result.option["series"]
    assert [base["datasetIndex"], fit["datasetIndex"]] == [1, 2]
    assert result.option["visualMap"]["seriesIndex"] == 0
    assert result.trends[0][1]["Stores"].tolist() == [61, 81]
    assert result.trends[0][1].iloc[:, 1].iloc[0] == pytest.approx(47.6962, abs=0.02)
    assert fit["encode"]["y"] in result.trends[0][1]
    doc.horizontal = True
    assert doc.build(df)["series"][1]["encode"]["x"] == fit["encode"]["y"]
    doc.transform.value = 81
    result = doc.compile(df)
    assert len(result.option["series"]) == 1 and not result.trends
    assert "distinct" in result.messages[0]


def test_rolling_average_uses_calendar_order_and_keeps_gaps():
    sample = SAMPLES["Monthly retail"]
    doc = Document.for_sample(sample, "Moving average")
    doc.transform.sort_field = "Revenue"
    result = doc.compile(sample.dataframe())
    _, trend = result.trends[0]
    assert trend["Month"].tolist()[:3] == ["Jan", "Feb", "Mar"]
    assert trend.iloc[:2, 1].isna().all()
    assert trend.iloc[2, 1] == 45
    sample = SAMPLES["Weather log"]
    result = Document.for_sample(sample, "Moving average").compile(sample.dataframe())
    assert result.trends[0][1].iloc[19:25, 1].isna().all()
    assert pd.notna(result.trends[0][1].iloc[25, 1])


def test_annotations_follow_fields_and_leave_unbound_fields_dormant():
    sample = SAMPLES["Monthly retail"]
    df = sample.dataframe()
    doc = Document.for_sample(sample, "Benchmarks and bands")
    s = doc.build(df)["series"][0]
    assert [r.get("type", r.get("yAxis")) for r in s["markLine"]["data"]] == [
        60,
        "average",
    ]
    assert [r["xAxis"] for r in s["markArea"]["data"][0]] == ["Apr", "Jun"]
    doc.horizontal = True
    s = doc.build(df)["series"][0]
    assert s["markLine"]["data"][0]["xAxis"] == 60
    assert s["markArea"]["data"][0][0]["yAxis"] == "Apr"
    doc.shared_x = "Target"
    assert "markArea" not in doc.build(df)["series"][0]
    doc.shared_x = "Month"
    assert len(doc.build(df)["series"][0]["markArea"]["data"]) == 1


def test_plot_and_value_axes_survive_rotation_panels_and_series_removal():
    sample = SAMPLES["Monthly retail"]
    df = sample.dataframe()
    doc = Document.for_sample(sample, "Linked panels")
    doc.horizontal = True
    doc.horizontal_axes["Month"] = {"inverse": True}
    base = doc.build(df)
    assert len(base["grid"]) == 2
    assert [axis["gridIndex"] for axis in base["yAxis"]] == [0, 1]
    assert all(axis["inverse"] for axis in base["yAxis"])
    assert base["axisPointer"]["link"] == [{"yAxisIndex": [0, 1]}]
    doc.series["Target"].x_override = "Revenue"
    assert "axisPointer" not in doc.build(df)
    doc.measures = ["Target"]
    assert isinstance(doc.build(df)["grid"], dict)
    assert "gridIndex" not in doc.build(df)["xAxis"]


def test_widgets_for_native_transforms_and_repeating_references():
    app = start("Rank the regions")
    key = "Regional channels:Rank the regions:dataset:"
    app.selectbox(key=key + "filter").select("Stores").run()
    app.number_input(key=key + "filter-value:Stores").set_value(60.0).run()
    spec = render(app)
    assert spec["dataset"][1]["transform"][0]["config"] == {
        "dimension": "Stores",
        "gte": 60.0,
    }
    assert spec["series"][0]["encode"] == {"x": "Stores", "y": "Region"}
    app.selectbox(key="example").select("Bar chart").run()
    scope = "Monthly retail:series:Revenue:bar:"
    app.button(key=scope + "markLine.data:add").click().run()
    app.button(key=scope + "markLine.data:add").click().run()
    doc = app.session_state["documents"]["Monthly retail"]
    a, b = doc.series["Revenue"].references
    app.selectbox(key=scope + b.uid + ":kind").select("Statistic").run()
    app.selectbox(key=scope + b.uid + ":stat").select("median").run()
    app.text_input(key=scope + b.uid + ":name").set_value("Median revenue").run()
    app.button(key=scope + a.uid + ":remove").click().run()
    lines = render(app)["series"][0]["markLine"]["data"]
    assert (
        len(lines) == 1
        and lines[0]["type"] == "median"
        and lines[0]["name"] == "Median revenue"
    )


def test_piecewise_boundaries_and_controls_are_independent_of_continuous_mapping():
    app = start("Heatmap")
    key = "Regional channels:Heatmap:visualMap:Sales:"
    app.selectbox(key=key + "type").select("piecewise").run()
    pieces = render(app)["visualMap"]["pieces"]
    assert (
        pieces[0]["lte"] == pieces[1]["gt"]
        and "gt" not in pieces[0]
        and "lte" not in pieces[-1]
    )
    cutoff = next(n.key for n in app.number_input if n.key.endswith(":limit"))
    app.number_input(key=cutoff).set_value(30.0).run()
    app.number_input(key=cutoff).set_value(10000.0).run()
    assert render(app)["visualMap"]["pieces"][0]["lte"] == 30
    app.button(key=key + "add-piece").click().run()
    assert len(render(app)["visualMap"]["pieces"]) == 4
    app.selectbox(key=key + "type").select("continuous").run()
    assert render(app)["visualMap"]["min"] == 18
    app.selectbox(key=key + "type").select("piecewise").run()
    assert render(app)["visualMap"]["pieces"][0]["lte"] == 30


def test_canvas_toolbar_note_aria_and_optional_branch_resets():
    app = start("Stacked bars")
    key = "Regional channels:Stacked bars:"
    branch(app, "Chart")
    app.text_input(key=key + "Chart:backgroundColor").set_value("#f7f2e4").run()
    app.button(key=key + "Chart:start").click().run()
    assert render(app)["backgroundColor"] == "#f7f2e4"
    assert len(render(app)["color"]) == 3
    app.button(key=key + "Chart:swatch:1:up").click().run()
    assert render(app)["color"][0] == "#dd8b45"
    branch(app, "graphic")
    app.toggle(key=key + "graphic:enabled").set_value(True).run()
    app.text_input(key=key + "graphic:style.text").set_value("Retail sample").run()
    app.selectbox(key=key + "graphic:corner").select("Top left").run()
    assert render(app)["graphic"]["elements"][0] == {
        "type": "text",
        "silent": True,
        "top": "2%",
        "left": "2%",
        "style": {"text": "Retail sample"},
    }
    branch(app, "toolbox")
    app.toggle(key=key + "toolbox:enabled").set_value(True).run()
    assert render(app)["toolbox"]["feature"] == {"dataZoom": {}, "restore": {}}
    app.toggle(key=key + "toolbox:feature.restore").set_value(False).run()
    assert "restore" not in render(app)["toolbox"]["feature"]
    branch(app, "aria")
    app.toggle(key=key + "aria:enabled").set_value(True).run()
    app.text_input(key=key + "aria:label.description").set_value(
        "Regional channels by sales"
    ).run()
    app.toggle(key=key + "aria:decal.show").set_value(True).run()
    assert render(app)["aria"] == {
        "enabled": True,
        "label": {"description": "Regional channels by sales"},
        "decal": {"show": True},
    }
    branch(app, "graphic")
    app.toggle(key=key + "graphic:enabled").set_value(False).run()
    assert "graphic" not in render(app)


def test_tooltip_labels_brush_and_media_are_real_echarts_paths():
    app = start("Scatter plot")
    scope = "Regional channels:Scatter plot:"
    series = scope + "series:Online:scatter:"
    app.multiselect(key=series + "tooltip-fields").set_value(
        ["Wholesale", "Region"]
    ).run()
    app.selectbox(key=series + "label-field").select("Region").run()
    app.selectbox(key=series + "labelLayout.moveOverlap").select("shiftY").run()
    s = render(app)["series"][0]
    assert (
        s["encode"]["tooltip"] == ["Wholesale", "Region"]
        and s["label"]["formatter"] == "{@Region}"
    )
    assert s["labelLayout"] == {"moveOverlap": "shiftY"}
    branch(app, "brush")
    app.toggle(key=scope + "brush:enabled").set_value(True).run()
    app.multiselect(key=scope + "brush:tools").set_value(["polygon"]).run()
    assert render(app)["brush"]["toolbox"] == ["polygon", "clear"]
    app.selectbox(key="example").select("Responsive layout").run()
    out = render(app)
    assert out["media"][0]["query"] == {"maxWidth": 500}
    assert "dataset" in out["baseOption"] and "dataset" not in out
    assert out["media"][-1]["option"]["legend"]["orient"] == "vertical"
    assert out["media"][0]["option"]["grid"] == {"right": "8%"}
    assert out["media"][-1]["option"]["grid"] == {"right": "24%"}
    app.button(key="Monthly retail:Responsive layout:media:add").click().run()
    assert len(render(app)["media"]) == 3


def test_overlapping_breakpoints_update_independent_edges_on_all_panels():
    sample = SAMPLES["Monthly retail"]
    doc = Document.for_sample(sample, "Linked panels")
    doc.enabled.add("media")
    doc.media_rules = [
        MediaRule("maxWidth", 500, "Bottom", "right", 7),
        MediaRule("minHeight", 630, "Left", "left", 12),
    ]
    baseline, narrow, tall = doc.build(sample.dataframe())["media"]
    assert baseline["query"] == {}
    assert baseline["option"]["grid"] == [{"left": "15%", "right": "10%"}] * 2
    assert narrow["option"]["grid"] == [{"right": "7%"}] * 2
    assert tall["option"]["grid"] == [{"left": "12%"}] * 2


def test_linear_fit_needs_numeric_scales_and_returns_when_restored():
    sample = SAMPLES["Regional channels"]
    df = sample.dataframe()
    doc = Document.for_sample(sample, "Linear fit")
    doc.axes["Stores"]["type"] = "category"
    assert doc.trend_methods("Online", df) == ["None"]
    result = doc.compile(df)
    assert len(result.option["series"]) == 1 and "value scale" in result.messages[0]
    doc.axes["Stores"].clear()
    doc.components["yAxis"]["type"] = "category"
    assert len(doc.build(df)["series"]) == 1
    doc.components["yAxis"].clear()
    assert len(doc.build(df)["series"]) == 2


def test_numeric_and_date_category_markers_follow_plotted_positions():
    sample = SAMPLES["Regional channels"]
    df = sample.dataframe()
    doc = Document.for_sample(sample, "Scatter plot")
    doc.axes["Stores"]["type"] = "category"
    ref = Reference("Fixed", "Stores", 61)
    doc.series["Online"].references.append(ref)
    doc.transform = Transform(sort_field="Stores", order="desc")
    assert doc.build(df)["series"][0]["markLine"]["data"][0]["xAxis"] == 2
    doc.transform.order = "asc"
    assert doc.build(df)["series"][0]["markLine"]["data"][0]["xAxis"] == 3
    doc.transform = Transform("Stores", "gte", 70)
    assert "markLine" not in doc.build(df)["series"][0]
    doc.transform = Transform()
    doc.shared_x = "Online"
    ref.column = "Online"
    ref.axis_when_shared = "xAxis"
    assert doc.build(df)["series"][0]["markLine"]["data"][0]["xAxis"] == 61

    sample = SAMPLES["Weather log"]
    doc = Document.for_sample(sample, "Benchmarks and bands")
    doc.axes["Date"]["type"] = "category"
    area = doc.build(sample.dataframe())["series"][0]["markArea"]["data"][0]
    assert [point["xAxis"] for point in area] == [15, 29]
