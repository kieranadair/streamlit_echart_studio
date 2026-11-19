# ECharts Studio

An interactive Apache ECharts reference built with Streamlit. Edit the option, see the chart respond, and inspect the Python that produced it. The app opens on a bar chart of monthly revenue.

The [30 Days of Apache ECharts course design](docs/course/README.md) explains how Tableau users can learn the option through the builder. It includes the syllabus, teaching sources, worked lessons, and pilot plan.

## Starting examples

| Example | What to try |
| --- | --- |
| Bar chart | Add a second Y field, then change its `series.type` to `line` to compare revenue with its target. |
| Stacked bars | All three sales channels share a `stack` name. Clear it on one series to move that channel beside the stack. |
| Area chart | Change `areaStyle.opacity` on the line. Reset it to remove the fill. |
| Scatter plot | Compare store and online sales for each region. Change the marker shape, size or opacity in the series tab. |
| Bubble plot | Open `visualMap` to see how wholesale sales set each point's size. Change the size range or choose **Fixed series.symbolSize** for equal-sized points. |
| Heatmap | Swap the two category fields to transpose the grid. Change the endpoints of `visualMap.inRange.color` or the scale limits to see how the same sales values read in colour. |
| Rank the regions | Filter to regions with at least 60 in **Stores**, then reverse the sort. Compare the source rows with the three bars that remain. |
| Benchmarks and bands | Move the revenue benchmark, change the mean line to a median, or extend the shaded Q2 band into July. |
| Linear fit | Filter out a region and inspect how the fitted endpoints and regression equation change. |
| Moving average | Change the trailing window from three observations to four and find the first month with a complete window. |
| Linked panels | Hover over June to read revenue and target on separate scales. Toggle `axisPointer.link` to explore them independently. |
| Responsive layout | Narrow the live chart below 500 px to move the legend beneath the plot and reclaim the right margin. |

Each example opens with a suggested dataset. You can switch among all three datasets and return to your edits within the session. Scatter, line and bar series can share a chart. A bubble plot uses a scatter series and a continuous `visualMap` scoped to that series. [Scatter series](https://echarts.apache.org/en/option.html#series-scatter) · [Continuous visual mapping](https://echarts.apache.org/en/option.html#visualMap-continuous)

## Explore an option

Choose a branch tab or search for a property by name or visual effect. Expanded groups show the hierarchy, such as `title.textStyle` and `series.emphasis.itemStyle`. Each row shows its current value beside its description. An edit updates the chart and marks the row as configured. Reset the row, or return a literal to its default, to omit that property. Automatic values such as `barWidth` stay unset until edited. Optional branches can be turned off while retaining their edits for the session.

The same pandas DataFrame supplies the data preview and the chart's `dataset.source`. For bar, line and scatter charts, each measure creates a series. Choose a shared X field under the preview or change `encode.x` for one series in the **series** tab. Distinct X fields get their own axes, connected through `series.xAxisIndex`. For example, in **Weather log**, add **Low** and map its X field to **Day** while **High** stays on **Date**. The **xAxis** tab lets you edit each scale. **Swap X and Y** shows how the same bindings work for a horizontal chart.

For a heatmap, the preview and chart use one row per cell. In **Regional channels**, the columns are **Region**, **Channel** and **Sales**. The category axes use `encode.x` and `encode.y`. The cell value uses `encode.value`, and `visualMap.dimension` identifies the same column by its zero-based index. Choose a continuous gradient or switch to `piecewise` and edit each band's cutoff, label and colour. [Heatmap series](https://echarts.apache.org/en/option.html#series-heatmap) · [Piecewise visual mapping](https://echarts.apache.org/en/option.html#visualMap-piecewise.pieces) · [ECharts dataset and encode](https://echarts.apache.org/handbook/en/concepts/dataset/)

**View ECharts option**, beneath the editor, shows the Python option sent to native `st.echarts_chart`. The variable `df` refers to the source DataFrame. Streamlit transports each DataFrame using Arrow. [Streamlit ECharts API](https://docs.streamlit.io/develop/api-reference/charts/st.echarts_chart)

### Data, annotations and interaction

- In **dataset**, filter by a field and sort the result. ECharts runs these steps in a second dataset. Open **Inspect plotted data** below the field selectors to compare the original rows with the transformed rows. [Dataset transforms](https://echarts.apache.org/handbook/en/concepts/data-transform/)
- In **series**, add named reference lines at a fixed value, mean, median, minimum or maximum. A reference band spans two positions on an axis. References follow their bound field when you swap axes. The same tab controls point labels, overlap handling and which fields appear in the tooltip. [markLine](https://echarts.apache.org/en/option.html#series-bar.markLine) · [markArea](https://echarts.apache.org/en/option.html#series-bar.markArea) · [labelLayout](https://echarts.apache.org/en/option.html#series-scatter.labelLayout)
- A calculated trend uses the filtered observations. Python fits a least-squares line to complete numeric pairs or computes a trailing mean in dimension order. Each result is a separate DataFrame and line series. **Inspect plotted data** shows its calculation and rows. The displayed option refers to these tables as `trend_df_1`, `trend_df_2`, and so on.
- Use **brush** to select bars or scatter points with a rectangle or polygon and style the marks inside and outside the selection. **toolbox** adds drag-to-zoom, zoom-back and restore. [Brush](https://echarts.apache.org/en/option.html#brush) · [Toolbox](https://echarts.apache.org/en/option.html#toolbox.feature)

### Canvas and layout

**Chart** controls the canvas background, series palette and inherited font. **grid** controls the plot background, border, outer bounds and margins. With multiple measures, split the plot into vertically stacked grids and link the pointers on their shared dimension. **title** and **legend** control placement, padding and backgrounds. [Grid](https://echarts.apache.org/en/option.html#grid) · [Linked axis pointers](https://echarts.apache.org/en/option.html#axisPointer.link)

Pin a source note in **graphic**, or use **aria** to describe the chart for screen readers and add patterned decals. In **media**, set breakpoints for width, height or aspect ratio and choose the legend position and grid inset for each layout. Adjust **Preview size** beside the live chart to cross a breakpoint. [Graphic elements](https://echarts.apache.org/en/option.html#graphic.elements) · [Responsive options](https://echarts.apache.org/en/option.html#media) · [Accessibility and decals](https://echarts.apache.org/handbook/en/best-practices/aria/)

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
