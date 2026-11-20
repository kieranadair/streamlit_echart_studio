# Writing and teaching a Studio lesson

A day is a short investigation carried out in ECharts Studio. The learner should leave with one explanation they can use again. The [syllabus](syllabus.md) supplies the investigation. This guide gives authors a consistent way to teach it.

## The seven parts of a lesson

1. **Meet the parameters.** Give the official path, its role, a concrete value, and its visible effect. Explain adjacent properties a learner could reasonably confuse.
2. **Set the challenge.** Name a reader and the decision this chart should help them make.
3. **Show the whole picture.** Present the finished comparison and its essential option fragment before taking it apart. In Studio, show the worked view when available.
4. **Know the dataset.** Give the grain, units, and a few real rows the learner can trace.
5. **Think it through.** Ask for a prediction, a reason, and an observation that could change their mind.
6. **Build, observe, explain.** Make one change at a time. Check a row, a mark, and an option path. Include a boundary or recovery exercise, then change the brief and let the learner choose the controls.
7. **Reflect.** Ask for an explanation that predicts a fresh case. Put the answer behind a reveal and link the relevant Apache reference.

Give more navigation help early and fade it as learners progress. Preserve conceptual explanations throughout. Measure how long each investigation actually takes during the solo pilot.

## Worked day 1

[Did March miss target?](day-01.md) follows a row through its axes and encodings, builds a mixed-series comparison and tests an independent reconstruction.

## Worked day 8

[Which regions qualify for review?](day-08.md) follows a source through a transform pipeline, tests an exact boundary, and separates eligibility, ranking and bar length.

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
