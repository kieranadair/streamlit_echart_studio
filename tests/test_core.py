import json

import pytest
from streamlit.testing.v1 import AppTest

from echarts_studio.data import SAMPLES
from echarts_studio.options import Document
from echarts_studio.schema import catalog, matches


@pytest.mark.parametrize("name", SAMPLES)
def test_complete_native_option(name):
    sample = SAMPLES[name]
    doc = Document.for_sample(sample)
    option = doc.build(sample)
    assert json.loads(json.dumps(option, allow_nan=False)) == option
    assert option["series"][0]["encode"] == {
        "x": sample.dimension,
        "y": sample.measures[0],
    }
    assert option["xAxis"]["type"] == ("time" if sample.time_axis else "category")


def test_search_by_effect_and_path():
    sections = catalog("bar", False)
    assert set(matches(sections, "space between bars")) >= {
        ("series", "barGap"),
        ("series", "barCategoryGap"),
    }
    assert ("xAxis", "axisLabel.rotate") in matches(sections, "xAxis.axisLabel.rotate")


def test_series_state_and_component_removal():
    sample = SAMPLES["Monthly retail"]
    doc = Document.for_sample(sample)
    doc.measures.append("Target")
    target = doc.series["Target"]
    target.settings("barWidth")["barWidth"] = "45%"
    target.kind = "line"
    target.settings("smooth")["smooth"] = False
    option = doc.build(sample)
    assert "barWidth" not in option["series"][1]
    assert option["series"][1]["smooth"] is False
    assert "smooth" not in option["series"][0]
    target.kind = "bar"
    assert doc.build(sample)["series"][1]["barWidth"] == "45%"
    doc.enabled.remove("tooltip")
    assert "tooltip" not in doc.build(sample)


def test_interactive_workflow():
    app = AppTest.from_file("../app.py").run()
    key = "Monthly retail"

    def series():
        return app.session_state["documents"][key].build(SAMPLES[key])["series"]

    include = f"{key}:series:barWidth:Revenue:bar:included"
    app.toggle(key=include).set_value(True).run()
    app.slider[0].set_value(65).run()
    assert series()[0]["barWidth"] == "65%"
    app.multiselect(key=key + ":measures").set_value(["Revenue", "Target"]).run()
    app.selectbox(key=key + ":active").select("Target").run()
    app.radio(key=key + ":Target:type").set_value("line").run()
    assert [s["type"] for s in series()] == ["bar", "line"]
    app.selectbox(key="dataset").select("Weather log").run()
    app.selectbox(key="dataset").select(key).run()
    assert series()[0]["barWidth"] == "65%"
    app.selectbox(key=key + ":active").select("Revenue").run()
    app.toggle(key=include).set_value(False).run()
    assert "barWidth" not in series()[0]
    app.multiselect(key=key + ":measures").set_value([]).run()
    assert not series()
    assert not app.exception
