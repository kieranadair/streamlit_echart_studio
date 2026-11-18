# ECharts Studio

An interactive Apache ECharts reference for line and bar charts, built with Streamlit. The app opens on a working bar chart with three bundled teaching datasets.

## Explore an option

Choose a branch tab or search for a property by name or visual effect. Expanded groups show the hierarchy, such as `title.textStyle` and `series.emphasis.itemStyle`. Each row shows its current value beside its description. An edit updates the chart and marks the row as configured. Reset the row, or return a literal to its default, to omit that property. Automatic values such as `barWidth` stay unset until edited. Optional branches can be turned off while retaining their edits for the session.

The same pandas DataFrame supplies the data preview and the chart's `dataset.source`. Each Y field creates a series. Choose a shared X field under the preview or change `encode.x` for an individual series in the **series** tab. Distinct X fields get their own axes, connected through `series.xAxisIndex`. For example, in **Weather log**, add **Low** and map its X field to **Day** while **High** stays on **Date**. In the **xAxis** tab you can then edit each scale independently.

**View ECharts option**, beneath the editor, shows the Python option with `df` referring to the selected DataFrame. Streamlit transports the chart data using Arrow. [Streamlit ECharts API](https://docs.streamlit.io/develop/api-reference/charts/st.echarts_chart)

## Run locally

Use Python 3.12 or 3.14 in a virtual environment.

```sh
python -m pip install -r requirements.txt
streamlit run app.py
```

For Streamlit Community Cloud, select the branch containing the app and the entrypoint `app.py`.

## Development

```sh
python -m pip install pytest
python -m pytest
```

The editable property catalog in `echarts_studio/schema.py` describes defaults for the built-in ECharts 6.1 renderer bundled with Streamlit 1.67.0. Each field has an official option path, a hint and a control type. A computed or inherited default has a placeholder explaining its behaviour. The chart uses `theme=None` so the controls follow the native ECharts defaults. [Apache ECharts option reference](https://echarts.apache.org/en/option.html)
