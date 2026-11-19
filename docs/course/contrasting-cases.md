# Three experiments where the picture is insufficient

A learner fluent in Tableau can often reproduce a picture before they understand its ECharts option. These short activities exploit that ability. Give the two starting conditions, invite a prediction, then ask the learner to choose a piece of evidence that would tell the conditions apart. Reveal the mechanism after they have a reason to want its name.

Schwartz and Bransford studied college students who actively compared cases from cognitive psychology before receiving an explanation. Comparison helped prepare students to learn from the explanation. Here we use that sequence to design experiments about chart configuration. Its effectiveness for this course is a question for the pilot. [A Time for Telling](https://aaalab.stanford.edu/papers/time_for_telling.pdf)

## 1 · The same ranking from opposite row orders

**Use on days 7 or 10.** Open Rank the regions with Regional channels and the full six regions. In A, sort Stores descending and enable `yAxis.inverse`. In B, sort Stores ascending and return `yAxis.inverse` to its default of false. Make one change at a time so the learner can see the intermediate view.

**Ask before opening the inspector.** “Eastern Seaboard is at the top in both finished charts. If I take the first row of the plotted table, which region do I get in each case?”

**Evidence.** In A, the first plotted row is Eastern Seaboard at 81. In B, it is Western Plains at 38. In both charts the six displayed categories run from Eastern Seaboard at the top to Western Plains at the bottom. The native sort chooses row order. The direction of the category axis determines where those rows appear. A screenshot of the settled chart cannot settle a disagreement about the first row. [ECharts transforms](https://echarts.apache.org/handbook/en/concepts/data-transform/) · [Category axis direction](https://echarts.apache.org/en/option.html#yAxis.inverse)

**Transfer.** A reader wants the largest region at the top and a colleague wants the first retained row to be the largest. Which configuration satisfies both requirements? Ask the learner how they would verify the answer after a filter.

## 2 · A policy threshold that happens to equal a statistic

**Use on days 16 or 20.** Start with Bar chart and Monthly retail. Add one named reference line to Revenue. For A, define it as Fixed at 63.5. For B, use the same name and style and define it as Statistic, median. Record the two results in sequence or compare in two fresh sessions.

**Ask before applying the filter.** “Both lines currently mark 63.5. The report will retain only months with Revenue of at least 50. What is the smallest intervention that will reveal which line was specified by policy?”

**Evidence.** The full-year median Revenue is 63.5. The nine-month median is 68. The fixed line stays at 63.5. On the original vertical chart, the fixed entry carries `yAxis: 63.5`. The other entry carries `type: "median"` and `valueDim: "Revenue"`. The policy and the statistic had the same value by coincidence. [ECharts reference lines](https://echarts.apache.org/en/option.html#series-bar.markLine) · [Data and checked values](datasets.md)

**Transfer.** Ask which definition to use for a contractual threshold and which to use for the typical month in the current report. Both are legitimate intentions. The option should preserve the chosen one as conditions change.

## 3 · A property whose effect is hidden by the data

**Use on days 12 or 19.** Open Area chart with Weather log and High. Sort Date ascending and filter Date to 1 May 2025 or later. In A use the default `connectNulls`. In B enable it. Compare the line in both conditions, then remove the date filter. Leave the sort enabled so the inspector remains available.

**Ask before removing the filter.** “The option changed and the May line looks identical. What observations would we need to tell whether the property works?”

**Evidence.** All 30 May High readings exist. When April comes back, its four missing High readings create the condition that matters. A shows an interruption. B draws across it. The source rows for 20–23 April still have missing High in both cases. Inspect those rows before making a claim about temperature. [Line series reference](https://echarts.apache.org/en/option.html#series-line.connectNulls) · [Weather sample](datasets.md)

**Transfer.** Try Low on a line over the same dates. Predict the result from the Low column before testing the setting. The learner can now explain why an invisible edit is sometimes the correct rendering.

## A prompt for a fourth case

Ask the learner to construct two plausible explanations for one observed chart, choose an edit that would make their predictions diverge, and identify a row or option path that would settle the question. This makes a short independent extension to the [capstone](assessment.md#capstone-briefs).
