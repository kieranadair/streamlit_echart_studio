# ECharts Studio

An interactive Apache ECharts option reference for line and bar charts, built with Streamlit. Open the app to explore a working chart with three bundled, illustrative datasets. Each dataset remembers its edits within the current browser session.

Browse an option branch or search for a property or visual effect. Include a property to edit it, or remove it to let ECharts choose its default. Configure series to add a measure or switch it between bar and line. Each series remembers its type-specific styles. The preview and the expandable JSON view use the same option.

## Run locally

Use Python 3.12 or 3.14 in a virtual environment.

```sh
python -m pip install -r requirements.txt
streamlit run app.py
```

For Streamlit Community Cloud select the repository branch containing the rebuild and the entrypoint `app.py`. The app requires Streamlit 1.67.0. Its teaching datasets are local, and its dependencies allow prebuilt NumPy wheels on Python 3.14.

## Development

```sh
python -m pip install pytest
python -m pytest
```

The editable property catalog lives in `echarts_studio/schema.py`. It covers a curated subset of native JSON-compatible ECharts options. Add an official path, example value, and hint to extend the explorer. The editor writes only explicitly included fields plus the chart's required structure. Data and document construction can be tested independently of Streamlit.
