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
        {"type": "sort", "config": {"dimension": "Stores", "order": "desc"}},
    ],
}
```

## 4. Know the dataset

Open **Rank the regions** with **Regional channels**, descending Stores and no filter. Sales are in thousands of dollars. For pencil-and-paper predictions, these pairs give Stores and Online respectively.

| Region | Stores | Online |
| --- | ---: | ---: |
| Eastern Seaboard | 81 | 57 |
| Central Valley | 67 | 50 |
| Pacific Northwest | 61 | 48 |
| Southern Highlands | 52 | 36 |
| Northern Coast | 43 | 39 |
| Western Plains | 38 | 31 |

## 5. Think it through

Write down the three qualifying names. Which table should still have six rows? Could a bar chart look reversed while the first row of its plotted table stays the same? Decide what evidence would settle that.

## 6. Build, observe, explain

1. In **dataset**, filter Stores with `gte` and 60. Compare the source preview with **Inspect plotted data**. Open **View ECharts option** and trace both dataset indices. One points upstream to the input. The other tells the series where to read its rows.
2. Raise the cutoff to 61. Predict before applying it. Now change only `gte` to `gt`. Name the row that disappeared and explain the single-character difference in the rule.
3. Try `gt` 81. Diagnose the empty chart using both tables. Recover by restoring `gte` 60. Which control brought back the bars?
4. Toggle `yAxis.inverse`. Record the top bar and first plotted row, then restore the axis. Switch the sort to ascending and record both again. Explain which operation changes the actual row order.
5. Take a new brief without following the recipe again. Keep regions with **Online sales of at least $50,000**, ordered by descending **Stores**, and use bar length for **Stores**. Inspect the filter dimension, sort dimension and X encoding. Why can three references to a field serve three different purposes?

## 7. Reflect and transfer

Your manager now wants Online sales to determine bar length too. Point to the binding that would need to change. Explain which rule already decides eligibility and which rule currently owns ranking.

<details><summary>Check the shortlist and boundary cases</summary>

Stores ≥ 60 retains Eastern Seaboard (81), Central Valley (67) and Pacific Northwest (61). At exactly 61, an inclusive cutoff keeps Pacific Northwest and a strict one drops it. No region exceeds 81. Inverting the axis preserves the first plotted row. Sorting the three qualifying rows ascending puts Pacific Northwest first in the table. The new Online brief retains Eastern Seaboard and Central Valley. Their bar lengths are still 81 and 67. Encoding Online on X would give lengths of 57 and 50.

</details>

[Apache ECharts transforms guide](https://echarts.apache.org/handbook/en/concepts/data-transform/)
