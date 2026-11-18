import json

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from echarts_studio.data import SAMPLES
from echarts_studio.options import Document, option_code
from echarts_studio.schema import catalog, matches


@pytest.mark.parametrize("name", SAMPLES)
def test_native_dataframe_and_displayed_option(name):
    sample = SAMPLES[name]
    df = sample.dataframe()
    doc = Document.for_sample(sample)
    option = doc.build(df)
    assert option["dataset"]["source"] is df
    assert option["series"] == [
        {
            "name": sample.measures[0],
            "type": "bar",
            "encode": {"x": sample.dimension, "y": sample.measures[0]},
        }
    ]
    assert option["xAxis"] == {"type": "time" if sample.time_axis else "category"}
    doc.enabled.add("title")
    doc.components["title"]["text"] = "A 'quoted' title"
    option = doc.build(df)
    namespace = {"df": df}
    exec(option_code(option), namespace)  # noqa: S102 -- exercise the generated example
    assert namespace["option"] == option


def test_distinct_x_fields_and_axis_settings():
    sample = SAMPLES["Monthly retail"]
    df = sample.dataframe()
    doc = Document.for_sample(sample)
    doc.measures.append("Target")
    doc.series["Target"].kind = "line"
    doc.series["Target"].x_override = "Revenue"
    doc.axes["Month"]["axisLabel.rotate"] = 45
    option = doc.build(df)
    assert option["xAxis"] == [
        {"type": "category", "axisLabel": {"rotate": 45}},
        {"type": "value"},
    ]
    assert [(s["xAxisIndex"], s["encode"]["x"]) for s in option["series"]] == [
        (0, "Month"),
        (1, "Revenue"),
    ]
    doc.shared_x = "Revenue"
    option = doc.build(df)
    assert option["xAxis"] == {"type": "value"}
    assert all("xAxisIndex" not in s for s in option["series"])
    doc.shared_x = "Month"
    doc.series["Target"].x_override = None
    assert doc.build(df)["xAxis"]["axisLabel"]["rotate"] == 45


def test_catalog_defaults_and_search():
    sections = catalog("bar", "category")
    assert set(matches(sections, "space between bars")) >= {
        ("series", "barGap"),
        ("series", "barCategoryGap"),
    }
    assert ("xAxis", "axisLabel.rotate") in matches(sections, "xAxis.axisLabel.rotate")
    assert sections["series"]["barWidth"].default is None
    assert sections["xAxis"]["axisLabel.rotate"].default == 0
    assert sections["xAxis"]["splitLine.show"].default is False
    assert sections["yAxis"]["splitLine.show"].default is True
    assert sections["title"]["textStyle.fontSize"].default == 18
    assert catalog("line", "time")["series"]["showSymbol"].default is True


def chart(app):
    assert not app.exception
    assert not app.warning
    proto = app.get("echarts_chart")[0].proto
    assert len(proto.datasets) == 1
    return json.loads(proto.spec)


def open_branch(app, name):
    app.session_state["option_branches"] = name
    app.run()


def test_direct_edit_defaults_resets_and_hidden_tabs():
    app = AppTest.from_file("../app.py").run()
    assert {tab.label for tab in app.tabs} >= {"series", "xAxis", "yAxis", "title"}
    bar = "Monthly retail:series:Revenue:bar:"
    assert app.number_input(key=bar + "barWidth").value is None
    assert app.number_input(key=bar + "barGap").value == 10
    assert "barGap" not in chart(app)["series"][0]
    app.number_input(key=bar + "barGap").set_value(45).run()
    assert chart(app)["series"][0]["barGap"] == "45%"
    app.number_input(key=bar + "barGap").set_value(10).run()
    assert "barGap" not in chart(app)["series"][0]
    app.number_input(key=bar + "barWidth").set_value(42).run()
    open_branch(app, "xAxis")
    assert chart(app)["series"][0]["barWidth"] == "42%"
    app.number_input(key="Monthly retail:xAxis:Month:axisLabel.rotate").set_value(
        25
    ).run()
    assert chart(app)["xAxis"]["axisLabel"] == {"rotate": 25}
    open_branch(app, "series")
    app.button(key=bar + "barWidth:reset").click().run()
    assert app.number_input(key=bar + "barWidth").value is None
    assert "barWidth" not in chart(app)["series"][0]


def test_branch_toggle_retains_edits_and_prunes_empty_parents():
    app = AppTest.from_file("../app.py").run()
    open_branch(app, "title")
    title = "Monthly retail:title:"
    assert app.number_input(key=title + "textStyle.fontSize").disabled
    app.toggle(key=title + "enabled").set_value(True).run()
    app.text_input(key=title + "text").set_value("Retail").run()
    app.number_input(key=title + "textStyle.fontSize").set_value(26).run()
    assert chart(app)["title"] == {"text": "Retail", "textStyle": {"fontSize": 26}}
    app.toggle(key=title + "enabled").set_value(False).run()
    assert "title" not in chart(app)
    app.toggle(key=title + "enabled").set_value(True).run()
    app.number_input(key=title + "textStyle.fontSize").set_value(18).run()
    assert chart(app)["title"] == {"text": "Retail"}


def test_dataset_switch_and_independent_series_bindings():
    app = AppTest.from_file("../app.py").run()
    key = "Monthly retail"
    app.multiselect(key=key + ":measures").set_value(["Revenue", "Target"]).run()
    app.selectbox(key=key + ":active").select("Target").run()
    app.selectbox(key=key + ":Target:type").select("line").run()
    app.selectbox(key=key + ":Target:encode.x").select("Target").run()
    option = chart(app)
    assert [s["type"] for s in option["series"]] == ["bar", "line"]
    assert option["series"][1]["xAxisIndex"] == 1
    assert option["series"][1]["encode"]["x"] == "Target"
    app.selectbox(key="dataset").select("Weather log").run()
    assert chart(app)["xAxis"]["type"] == "time"
    assert pd.api.types.is_datetime64_any_dtype(
        SAMPLES["Weather log"].dataframe()["Date"]
    )
    app.selectbox(key="dataset").select(key).run()
    assert chart(app)["series"] == option["series"]
    app.multiselect(key=key + ":measures").set_value([]).run()
    assert not app.get("echarts_chart")
    assert not app.exception


def test_search_directly_edits_nested_fields_and_auto_boolean():
    app = AppTest.from_file("../app.py").run()
    app.text_input(key="property_search").set_value("axisLine.show").run()
    assert [tab.label for tab in app.tabs] == ["xAxis", "yAxis"]
    open_branch(app, "yAxis")
    key = "Monthly retail:yAxis:axisLine.show"
    assert app.selectbox(key=key).value is None
    app.selectbox(key=key).select(False).run()
    assert chart(app)["yAxis"]["axisLine"]["show"] is False
    app.button(key=key + ":reset").click().run()
    assert app.selectbox(key=key).value is None
    assert "axisLine" not in chart(app)["yAxis"]


def test_multiple_x_axes_in_the_weather_lesson():
    app = AppTest.from_file("../app.py").run()
    app.selectbox(key="dataset").select("Weather log").run()
    app.multiselect(key="Weather log:measures").set_value(["High", "Low"]).run()
    app.selectbox(key="Weather log:active").select("Low").run()
    app.selectbox(key="Weather log:Low:encode.x").select("Day").run()
    assert [axis["type"] for axis in chart(app)["xAxis"]] == ["time", "value"]
    open_branch(app, "xAxis")
    app.selectbox(key="Weather log:axis").select("Day").run()
    app.text_input(key="Weather log:xAxis:Day:name").set_value("Observation day").run()
    assert chart(app)["xAxis"] == [
        {"type": "time"},
        {"type": "value", "name": "Observation day"},
    ]


def test_colour_picker_initialisation_preserves_automatic_colour():
    app = AppTest.from_file("../app.py").run()
    key = "Monthly retail:series:Revenue:bar:itemStyle.color"
    picker = key + ":swatch"
    # Browsers may echo the swatch as uppercase hex while mounting a tab.
    app.color_picker(key=picker).set_value(
        app.color_picker(key=picker).value.upper()
    ).run()
    assert "itemStyle" not in chart(app)["series"][0]
    app.color_picker(key=picker).set_value("#007755").run()
    assert chart(app)["series"][0]["itemStyle"] == {"color": "#007755"}
    app.button(key=key + ":reset").click().run()
    assert app.text_input(key=key).value == ""
    assert "itemStyle" not in chart(app)["series"][0]
