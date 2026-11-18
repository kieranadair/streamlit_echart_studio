# ECharts Studio

An interactive Apache ECharts reference built with Streamlit. Edit the option, see the chart respond, and inspect the Python that produced it. The app opens on a bar chart of monthly revenue.

## Starting examples

| Example | What to try |
| --- | --- |
| Bar chart | Add a second Y field, then change its `series.type` to `line` to compare revenue with its target. |
| Stacked bars | All three sales channels share a `stack` name. Clear it on one series to move that channel beside the stack. |
| Area chart | Change `areaStyle.opacity` on the line. Reset it to remove the fill. |
| Scatter plot | Compare store and online sales for each region. Change the marker shape, size or opacity in the series tab. |
| Bubble plot | Open `visualMap` to see how wholesale sales set each point's size. Change the size range or choose **Fixed series.symbolSize** for equal-sized points. |
| Heatmap | Swap the two category fields to transpose the grid. Change the endpoints of `visualMap.inRange.color` or the scale limits to see how the same sales values read in colour. |

Each example opens with a suggested dataset. You can switch among all three datasets and return to your edits within the session. Scatter, line and bar series can share a chart. A bubble plot uses a scatter series and a continuous `visualMap` scoped to that series. [Scatter series](https://echarts.apache.org/en/option.html#series-scatter) · [Continuous visual mapping](https://echarts.apache.org/en/option.html#visualMap-continuous)

## Explore an option

Choose a branch tab or search for a property by name or visual effect. Expanded groups show the hierarchy, such as `title.textStyle` and `series.emphasis.itemStyle`. Each row shows its current value beside its description. An edit updates the chart and marks the row as configured. Reset the row, or return a literal to its default, to omit that property. Automatic values such as `barWidth` stay unset until edited. Optional branches can be turned off while retaining their edits for the session.

The same pandas DataFrame supplies the data preview and the chart's `dataset.source`. For bar, line and scatter charts, each Y field creates a series. Choose a shared X field under the preview or change `encode.x` for an individual series in the **series** tab. Distinct X fields get their own axes, connected through `series.xAxisIndex`. For example, in **Weather log**, add **Low** and map its X field to **Day** while **High** stays on **Date**. In the **xAxis** tab you can then edit each scale independently.

For a heatmap, the preview and chart use one row per cell. In **Regional channels**, the columns are **Region**, **Channel** and **Sales**. The two category axes use `encode.x` and `encode.y`. The cell value uses `encode.value`, and `visualMap.dimension` identifies the same column by its zero-based index. The colour scale starts at the observed minimum and maximum. [Heatmap series](https://echarts.apache.org/en/option.html#series-heatmap) · [ECharts dataset and encode](https://echarts.apache.org/handbook/en/concepts/dataset/)

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
