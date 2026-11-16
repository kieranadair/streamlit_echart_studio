# ECharts Studio for Streamlit

A maintainable, dataset-aware educational workbench for native `st.echarts_chart()`.

## Why this architecture

- **No hardcoded sample data.** Browse Altair 6's `altair.datasets.data` catalog, loaded on demand, or upload CSV/Excel/Parquet/JSON.
- **Dataframe-first.** The normal path is `dataset.source = df` plus named `series.encode` mappings.
- **Schema-driven widgets.** `echarts_studio/schema.py` describes ECharts options; `ui.py` renders the appropriate Streamlit widget.
- **Separation of concerns.** Dataset/profile logic, schema, nested-option construction, UI rendering and export are separate modules.
- **Escape hatch.** Advanced JSON overlay supports JSON-compatible ECharts properties that do not yet have a widget.
- **Learning feedback loop.** Every UI change immediately updates the chart, option tree and copy-ready Python.

## Native Streamlit boundaries

The app targets Streamlit's native `st.echarts_chart`. Specs must be JSON-compatible, so JavaScript callbacks are deliberately not generated. Custom series requiring `renderItem`, registered GeoJSON maps and ECharts GL are also outside native-mode scope.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Altair sample datasets are discovered from `altair.datasets.data`. Many are remote, so loading them requires internet connectivity. Uploads work without network access.

## Extend

Add fields to `echarts_studio/schema.py`; the generic renderer handles bool/select/text/colour/integer/float widgets and nested option paths. Add new chart-type series schemas to the `SERIES` dictionary.
