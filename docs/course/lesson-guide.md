# Writing and teaching a Studio lesson

A day is a short investigation carried out in ECharts Studio. The learner should leave with one explanation they can use again. The [syllabus](syllabus.md) supplies the investigation. This guide gives authors a consistent way to teach it.

## The shape of a day

| Time to try in the pilot | What the learner does | What the author provides |
| --- | --- | --- |
| First 2 minutes | Opens a working chart and names a decision a reader could make. Recalls one relevant idea from an earlier day. | An exact starter, dataset, and any edits needed to reproduce the starting state in a fresh session. |
| Next 2 minutes | Commits to a prediction about a mark, a row count, a coordinate, or an option path. | One question with a meaningful alternative prediction. A learner can record an answer on paper or say it aloud. |
| Next 6–8 minutes | Changes one thing, observes the result, and inspects the smallest useful piece of the contract or data. | A short hint ladder and one way to recover from the most likely wrong turn. |
| Last 5–8 minutes | Puts the idea to work on a second field, boundary, or audience. Checks a value and explains the result in ECharts terms. | A check the learner can reveal after trying, a link to the relevant part of the official reference, and a small reconstruction note for later. |

A learner who predicts incorrectly has something precise to investigate. Ask them to choose the next observation that would distinguish their explanation from another one. If a learner gets the result by chance, change the field or condition and ask for the next prediction.

**Fade guidance deliberately.** On days 1–5 name both control and property. On days 6–15 give the task first and let learners reveal the branch. On days 16–25 ask for the mechanism and evidence before the recipe. On days 26–30 provide a reader brief and the references. A learner can request any hint early. Record which hint made the concept click during the pilot.

## Copyable lesson template

```markdown
# Day NN · [Question a reader wants answered]

**Starting state.** [Named example, dataset, bindings, optional branches,
and a short fresh-session recipe. Include a previously learned idea to recall.]

**Your task.** [A decision to make and one observable success condition.]

**Predict.** [What will change? Give a specific mark, value, or option path.]

**Try it in Studio.** [The smallest useful edit. Leave one choice to the learner.]

**Find the evidence.** [One row or computed value, one native option path,
and what the chart should let a reader see.]

**If you get stuck.** [Hint 1 names the concept. Hint 2 gives the branch.
Hint 3 gives the exact control and a recovery step.]

**Try a changed case.** [New field, threshold, scale, or reader constraint.]

<details>
<summary>Check your reasoning</summary>

[Expected outcome, acceptable alternatives, and a short explanation.
Give a text or table route for checks that otherwise depend on colour or hover.]

</details>

**Take away.** [One sentence the learner completes and one reference link.]
```

A learner can use four lines in their own notes for the **starting state**, **prediction**, **evidence**, and **next variation**. Copy a short option fragment if it helps recreate the experiment. The complete chart and a screenshot are optional.

## Worked day 1

**Learner brief.** You are preparing a retail review. Your colleague says March was on target. Use a single chart to check that claim, then explain how the same data supplies both marks.

**Start.** Open **Bar chart** with **Monthly retail**. Confirm Month is the shared X field and Revenue is the only Y field. In the preview locate the March row. Revenue and Target use thousands of dollars.

**Predict.** If you add Target, will March need another source row? Where should the target sit relative to the top of the March bar?

**Try it.** Add Target under **Y fields · encode.y**. In **series**, set **Edit series** to Target and choose `line` for `series.type`. Leave Revenue as a bar. Give a colleague the decision before opening the option. Then open **View ECharts option** and find the two entries under `series`. These are the relevant fields from the starter after that edit.

```python
[
    {"name": "Revenue", "type": "bar", "encode": {"x": "Month", "y": "Revenue"}},
    {"name": "Target", "type": "line", "encode": {"x": "Month", "y": "Target"}},
]
```

**Hints.** First ask which field would let a reader compare actual performance with expectation. Then look under the field selectors and the series tab. If both measures appear as bars, edit the series named Target. If Revenue became the line, select Revenue, return it to bar, and set Target to line.

**Try a changed case.** Is February’s result the same? Remove Target from the selected fields. Predict whether the Target column will still be in the data preview. Restore it and explain where the choice to draw a line lives.

<details>
<summary>Check the values and the contract</summary>

March shows 45 against 49, a shortfall of $4,000. February shows 48 against 46, $2,000 above target. The March observations share one source row. Both encodings read Month, while the two Y encodings choose different columns. Removing Target from the plotted measures leaves the source column available. The preview exposes both rows without requiring a hover gesture.

</details>

**Take away.** Finish “To find the value behind the Target line, I would follow …”. [Apache’s dataset and encoding guide](https://echarts.apache.org/handbook/en/concepts/dataset/)

## Worked day 16

**Learner brief.** A manager asks whether raising the sales threshold for the months included in a report will also raise its fixed benchmark. There are two horizontal lines in the view. Decide which can move, and explain who computes the new value.

**Start.** Open **Benchmarks and bands** with **Monthly retail** and the full twelve months. Confirm Revenue is on Y and the reference lines are Benchmark and Mean. If revisiting an edited session, restore the Fixed Revenue line to 60, the statistical Revenue line to average, and the dataset filter to None. Keep the Q2 band available as a landmark.

**Predict before editing.** Write down a direction or a value for each line if the report retains only months with Revenue ≥ 50. Give a reason for each prediction.

**Try it.** In **dataset** choose Revenue as the filter dimension, `gte` as the operator, and 50 as the value. Open **Inspect plotted data**. Count the retained records and check their total. In **View ECharts option**, locate the new dataset transform, the series using that dataset, and the two objects in `markLine.data`. The relevant parts of those objects read as follows.

```python
{"name": "Benchmark", "yAxis": 60}
{"name": "Mean", "type": "average", "valueDim": "Revenue"}
```

These are excerpts. The full entries also contain label and line styling. Look for the *rule* that lets the renderer determine the second position. Add a third reference line of type Statistic, choose median for Revenue, and give it a name.

**Hints.** Which line depends on the observations? Follow the series’ `datasetIndex` before inspecting its annotation. If the fixed line moves, check whether its definition was changed to Statistic. If the average seems wrong, check whether the filter field is Revenue or Target.

**Try a changed case.** Keep the plotted measure and statistical line on Revenue. Switch the filter field to Target, then set its value to 60 after the new field appears. Confirm the generated condition is **Target ≥ 60**. Does the mean line now describe Target, or does it describe Revenue for a different set of months?

<details>
<summary>Check the values and the contract</summary>

The original mean Revenue is 781 ÷ 12 ≈ 65.08. After Revenue ≥ 50, the nine retained months contribute 646. Their mean is about 71.78 and their median is 68. The explicit benchmark remains at 60. The statistical entry specifies `valueDim="Revenue"` and `type="average"`. ECharts calculates its position on the series data.

In the changed case, seven months qualify on Target. Revenue in those months totals 526, so the new mean Revenue is about 75.14. The filter field determines membership and the statistic’s field determines what is averaged. The two inspected tables and the two option entries are also a text-based route through the experiment.

</details>

**Take away.** Finish “A rule that chooses rows and a rule that computes a line can refer to different fields because …”. [Dataset transforms](https://echarts.apache.org/handbook/en/concepts/data-transform/) · [Reference lines](https://echarts.apache.org/en/option.html#series-bar.markLine)

## Author review before piloting

- Run the start from a fresh session. Try again with the likely edits left from the prior day. State the short path back to the intended starting state.
- Perform the learner’s edit in the current builder. Check the chart, authored option, and applicable DataFrame against the expected value. Name which layer supplies a default or calculation.
- Open the official reference at the property being taught. A UI-only convenience such as **Preview size** needs its own explanation.
- Try the changed case without using the worked steps. Keep a hint that helps diagnose the mistake while leaving the learner a decision.
- Check that a person using the text or table route can test the central claim. For a pointer-specific gesture, provide the underlying field values, option paths, and a companion demonstration. Include a real assistive-technology review before describing the published experience as accessible.
