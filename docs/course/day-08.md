# Day 8 · Which regions qualify for review?

## 1. Meet the parameters

| Option | Question it answers |
| --- | --- |
| `dataset[0].source` | Where are the original six rows? Index 0 means the first dataset. |
| `dataset[1].fromDatasetIndex` | Which dataset supplies input to this derived table? A value of 0 points back to the source. |
| `transform.type` and `transform.config` | Which operation runs and with what settings? A filter keeps rows meeting a condition on a named dimension. A sort orders the survivors by a named dimension. An array runs the operations in sequence. |
| `series[0].datasetIndex` | Which table supplies the marks? A value of 1 selects the derived table. |
| `series[0].encode` | Which columns from that table supply coordinates? Here Stores gives bar length on X and Region supplies the category on Y. |
| `yAxis.inverse` | Which direction do categories run on screen? This changes where the first category appears. |

## 2. The challenge

Your regional manager will review territories with store sales of at least $60,000. Give them a ranked shortlist and keep the original table available to explain exclusions.

## 3. See the whole picture

The finished view has three horizontal bars, largest at the top. The data journey is six source rows → filter → sort → three plotted rows → three bars. These are the native settings to find inside the derived dataset.

```python
{
    "fromDatasetIndex": 0,
    "transform": [
        {"type": "filter", "config": {"dimension": "Stores", "gte": 60}},
        {"type": "sort", "config": {"dimension": "Stores", "order": "desc", "incomparable": "min"}},
    ],
}
```

## 4. Know the dataset

Open **Rank the regions** with **Regional channels**, descending Stores and no filter. Sales are in thousands of dollars. For predictions, use this copy of the source ordered by Stores. Studio’s original table starts with Pacific Northwest.

| Region | Stores | Online | Wholesale |
| --- | ---: | ---: | ---: |
| Eastern Seaboard | 81 | 57 | 32 |
| Central Valley | 67 | 50 | 21 |
| Pacific Northwest | 61 | 48 | 20 |
| Southern Highlands | 52 | 36 | 28 |
| Northern Coast | 43 | 39 | 26 |
| Western Plains | 38 | 31 | 18 |

## 5. Think it through

Write down the three qualifying names. Which table should still have six rows? Could a bar chart look reversed while the first row of its plotted table stays the same? Decide what evidence would settle that.

## 6. Build, observe, explain

### Investigation A · Write a boundary test (7 minutes)

**Challenge.** Give the manager a qualifying headcount for Stores ≥ 60, ≥ 61, > 61 and > 81. Predict where two thresholds give the same result and where one record will drop out.

**Action.** Implement the four rules under **dataset** and check each in **Inspect plotted data**. For the empty chart, follow the series’ dataset index to the derived table and its parent. Show where all six records still exist. Restore ≥ 60.

**Reflect.** Write an acceptance test that would fail if someone changed an inclusive operator to a strict one. Explain why using 60 as your only test threshold would miss that bug.

### Investigation B · Debug a correct-looking shortlist (7 minutes)

**Challenge.** The manager requires both the table and the chart to read largest first. Could the chart pass a screenshot review while the table fails?

**Action.** Starting with descending Stores and the inverse category axis enabled, record the first plotted row and top bar. Change sort to ascending. Before toggling the axis direction, predict whether doing so will restore the original top bar. Check both table and chart. Draw the two paths from source to screen and identify the first place they differ.

**Reflect.** Give the manager two checks that together distinguish the correct specification from its convincing imitation. Restore descending sort and inverse axis.

### Investigation C · Separate admission, rank and magnitude (8 minutes)

**Challenge.** Admit regions with Online sales of at least $36,000, rank them by Online sales and show their **Stores** sales as bar lengths. A reviewer assumes bars should decrease smoothly down the page. Decide whether that is a valid acceptance test.

**Action.** Build this version without a control-by-control recipe. Locate the filter and sort dimensions in the transform array and the bar-length field in the series. Pick two neighbouring regions that would trade places if a colleague sorted by bar length. Deliberately introduce that error and use your pair to diagnose it. Repair the ranking, then change the threshold to strictly above $36,000. Check the boundary row.

**Reflect.** Write a chart title that communicates all three rules. Explain why the new threshold can make the sorting bug harder to see.

## 7. Reflect and hand over (4 minutes)

The manager changes the last clause to “show Wholesale sales.” Predict which field binding changes and what happens to membership and order. Make the change with the measure selector. Give a colleague a three-clause specification, a boundary case and a pair of amounts they can verify.

<details><summary>Check after the handover</summary>

For Stores, the four qualifying counts are 3, 3, 2 and 0. Pacific Northwest (61) witnesses the strict boundary. Descending sort with inverse enabled and ascending sort with inverse disabled both put Eastern Seaboard at the top. Only the former also puts it first in the plotted table.

Online ≥ 36 admits five regions. Northern Coast (Online 39, Stores 43) precedes Southern Highlands (Online 36, Stores 52). The longer bar legitimately comes later. Strictly above 36 removes Southern Highlands, eliminating that telltale reversal. The surviving order is Eastern Seaboard, Central Valley, Pacific Northwest and Northern Coast. Switching the bar measure to Wholesale gives 32, 21, 20 and 26 in that order. The filter and sort still refer to Online.

</details>

[Apache ECharts transforms guide](https://echarts.apache.org/handbook/en/concepts/data-transform/)
