# Day 1 · Did March miss target?

## 1. Meet the parameters

Think of putting Month on Columns and Revenue on Rows in Tableau. ECharts lets you describe three decisions separately. Which fields supply the coordinates? How does each axis position those coordinates? What draws the marks?

| Option in this chart | What ECharts does with it |
| --- | --- |
| `dataset.source` | Supplies the table. A named column in that table is a **dimension**. |
| `series[0].encode.x: "Month"` | Reads the Month cell from each row for the first series’ horizontal coordinate. The zero means the first entry in the series list. |
| `xAxis.type: "category"` | Gives each distinct month label a slot at equal intervals. A label such as Mar occupies a slot even though ECharts has no calendar date for it. |
| `series[0].encode.y: "Revenue"` | Reads the Revenue cell in the same row for the vertical coordinate. |
| `yAxis.type: "value"` | Places that number on a linear numeric scale. A difference of four units spans the same distance anywhere on this axis. |
| `series[0].type: "bar"` | Draws a bar reaching the encoded coordinate. A line series connects successive coordinates. |
| `series[0].name: "Revenue"` | Labels the series in a legend or tooltip when shown. Studio takes this label from the measure. ECharts reads the column named by the encoding. |

## 2. The challenge

A colleague says March met target. Build one view that lets them check March and then ask the same question about any month.

## 3. See the whole picture

Picture twelve Revenue bars with a Target line crossing them. The March bar should end below the March point on the line. Here is the part of the finished option that makes the comparison possible. Read across each series, then look up at the shared axes.

```python
{
    "xAxis": {"type": "category"},
    "yAxis": {"type": "value"},
    "series": [
        {"name": "Revenue", "type": "bar", "encode": {"x": "Month", "y": "Revenue"}},
        {"name": "Target", "type": "line", "encode": {"x": "Month", "y": "Target"}},
    ],
}
```

## 4. Know the dataset

Open **Bar chart** with **Monthly retail**. Start with Month on X and Revenue alone on Y. Find these source rows in the preview. One row represents one month, and both measures use thousands of dollars.

| Month | Revenue | Target |
| --- | ---: | ---: |
| Jan | 42 | 45 |
| Feb | 48 | 46 |
| Mar | 45 | 49 |

## 5. Think it through

Trace the March bar with your finger. Which property supplies “Mar”? Which one makes room for it? Which one supplies 45? If you replace Revenue with Target, predict the new March endpoint and name the two axis settings you expect to see afterwards.

## 6. Build, observe, explain

1. Open **View ECharts option**. Find the first series. Follow its X and Y bindings back to the March row. Say what the number 45 measures before looking at the bar.
2. Add Target under **Y fields · encode.y**. Inspect March and February. Find the second series in the option. Why can a second endpoint appear without adding any rows?
3. In **series**, select Target under **Edit series** and change its type to line. Inspect the option again. Find the property that changed. Check whether the March target moved vertically. If Revenue became the line, restore its type and select Target.
4. Remove Revenue from the selected measures, leaving Target. Find the single remaining Y encoding. Compare the March endpoint with your prediction. The scale can choose fresh tick limits when the plotted values change. Its type still describes numeric distance.
5. Rebuild the comparison with Revenue as bars and Target as a line. Use the chart to identify every missed month, then check those rows in the preview. Work out the February surplus and March shortfall in dollars.

## 7. Reflect and transfer

A colleague proposes changing the axis type to switch from actuals to targets. Show them the smallest edit that chooses a different measure. Explain how you could draw the exact same coordinates as a line.

<details><summary>Check your explanation</summary>

Both series read Mar for X. The category axis places them in the March slot. Their Y fields supply 45 and 49, so the numeric axis puts the target four units higher. February exceeded target by $2,000 and March missed by $4,000. January, March, June and September missed. Changing the field changes the coordinates. Changing the series type changes how those coordinates are drawn.

</details>

[Apache ECharts dataset and encoding guide](https://echarts.apache.org/handbook/en/concepts/dataset/)
