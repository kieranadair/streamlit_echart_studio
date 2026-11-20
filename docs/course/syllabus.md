# 30-day syllabus

**Course outcome.** Given a reader’s question and a supported DataFrame, a learner can design a chart in Studio, read its ECharts option, and adapt it to a change they did not rehearse.

Each day has one experiment and one check. The final column is an **author’s answer key**. Reveal it after the learner has predicted and tried the change. Use the seven-part format in the lesson guide. Calibrate depth using the solo pilot, including time spent on independent transfer. A learner can spread a section over more than one week. All core starts below use the current builder. The [dataset guide](datasets.md) maps optional transfer datasets to the sections.

**Starting a day.** Select the named **Starting example** and **Dataset**. Studio remembers edits to that combination during a session. Restore the specified fields or open a fresh session for the published starting state. A short recipe reproduces the prior day wherever a day depends on it. Keep a small personal note of predictions and option fragments for later reconstruction. [Worked lesson format](lesson-guide.md) · [Studio field guide](studio-reference.md)

## Days 1–5 · From a Tableau question to an ECharts option

Use a worked example first. Name the control as well as the official property. Gradually ask the learner to point to the relevant option before opening a hint.

| Day and question | Starting view | Experiment | Evidence to look for |
| --- | --- | --- | --- |
| [**01 · Did March miss target?**](day-01.md) | Bar chart · Monthly retail | Add Target as a second Y field. Set only Target to `line`. Compare March on the chart and in the first three rows. | March Revenue = 45 and Target = 49, both in thousands of dollars. Two series read one source. The Target series binds Y to Target. |
| **02 · What makes one mark?** | Bar chart · Monthly retail, Revenue and Target | Follow February from its source row through the two `encode` entries. Remove and restore Target. | A single February row supplies 48 and 46. Removing the series changes the chart while the DataFrame still contains Target and twelve rows. |
| **03 · Where did the horizontal scale come from?** | Bar chart · Weather log, High | Change the shared X field from Date to Day. Make a prediction about mark positions, tick text, and scale type. | For the first row, the same High of 17 °C can sit at 1 April or at day 1. `encode.x` and `xAxis.type` explain why equally spaced daily observations can look similar on two different scales. |
| **04 · Where is the default?** | Bar chart · Monthly retail | Rotate the month labels to 30°, inspect `xAxis.axisLabel.rotate`, then return it to 0°. | The edited leaf appears and then disappears from the authored option. Labels still render. The learner distinguishes the effective default from an explicit value. |
| **05 · Can you rebuild the comparison?** | Bar chart · Monthly retail, Revenue only | Reconstruct the day 1 view from the retail question. Choose which series should be visually prominent and defend it. | Trace one missed target to a row, name both Y bindings, and identify a property ECharts supplies by default. Accept more than one legible design. |

## Days 6–10 · Orientation, row order, and axis order

Use a six-row table that can be checked by eye. Give the desired behaviour before naming the branch. The distinction between changing rows and changing their presentation comes back on days 16 and 22. [Two ways to make the same ranking](contrasting-cases.md)

| Day and question | Starting view | Experiment | Evidence to look for |
| --- | --- | --- | --- |
| **06 · What makes a bar horizontal?** | Bar chart · Regional channels, Stores | Use **Swap X and Y**. Trace Pacific Northwest to its axes before and after. | Stores moves onto the value X axis and Region onto the category Y axis. The Pacific Northwest value stays 61. |
| **07 · Why is the largest bar at the top?** | Rank the regions · Regional channels | Hold the descending Stores sort fixed and toggle `yAxis.inverse`. Restore it, then change only the sort to ascending. | Flipping the axis leaves the plotted table in its previous order. Reversing the sort changes the first plotted row from Eastern Seaboard (81) to Western Plains (38). |
| [**08 · Which rows reach the chart?**](day-08.md) | Rank the regions · Regional channels, descending | Filter Stores to `gte` 60. Predict the survivors, then inspect the source and plotted tables. | Six rows enter and three reach the series, with Stores of 81, 67, and 61. The source is `dataset[0]` and the series uses the transformed dataset at index 1. |
| **09 · When do two series need two axes?** | Bar chart · Weather log, High and Low | Keep High on Date. Override the dimension for Low to Day in the series editor. Compare with both on Date. | The distinct bindings create two X axes and the series identify them with `xAxisIndex`. Sharing Date again lets them use one axis. Ask whether the extra scale helps this reader. |
| **10 · Debug a plausible ranking** | Rank the regions · Regional channels | Show the largest qualifying Stores value at the top. Compare “at least 61” with “above 61”. Explain how a reversed axis could conceal a mistaken sort. | Pacific Northwest appears for `gte` 61 and drops out for `gt` 61. Eastern Seaboard (81) and Central Valley (67) remain. The explanation accounts for the rows *and* the screen order. |

## Days 11–15 · How the same numbers become different marks

Use a familiar regional sales question to introduce stacking, position, size, and colour. Hints can name the relevant branch. Leave visual judgments, including whether to connect a gap, with the learner.

| Day and question | Starting view | Experiment | Evidence to look for |
| --- | --- | --- | --- |
| **11 · Is this total still a total?** | Stacked bars · Regional channels | Inspect the shared `stack` value, then clear it on Wholesale only. | Pacific Northwest starts with 61 + 48 + 20 = 129. The remaining stacked pair totals 109 and Wholesale contributes a separate bar of 20. All three source values survive. |
| **12 · What does a line across a gap claim?** | Area chart · Weather log, High | Toggle `connectNulls`, then change `areaStyle.opacity`. Describe the reading a viewer might take from each treatment. | High is missing on 20–23 April. A connecting segment can span the interval. Neither action creates a temperature measurement for those dates. |
| **13 · Which field sets a bubble’s size?** | Scatter plot · Regional channels | Establish Stores on X and Online on Y. Map Wholesale to `visualMap.inRange.symbolSize` and switch back to fixed size. | Eastern Seaboard stays at (81, 57). Its Wholesale value of 32 gives it the largest mapped marker. The learner finds the mapping’s dimension and targeted series. |
| **14 · What is one heatmap cell?** | Heatmap · Regional channels | Follow a Pacific Northwest cell from the long table to a colour. Swap the Region and Channel axes. | There are 18 Region–Channel rows. Pacific Northwest × Online still encodes 48. Only the axes swap. `encode.value` and `visualMap.dimension` still refer to Sales. |
| **15 · Which side owns the boundary?** | Heatmap · Regional channels | Switch to `piecewise`. With the upper cutoff of the first band at 39, predict the colour of Northern Coast × Online. Move that cutoff to 38. Choose meaningful band labels. | The value 39 moves into the middle band. A value of 38 stays in the first. The learner can read `lte` and `gt` in the option and justify whether bands suit this comparison. |

## Days 16–20 · References, calculations, and the observations behind them

Ask for a prediction before showing where to edit. Learners now distinguish an interval on an axis, a statistic ECharts computes, and a table calculated in Python. [Worked day 16](lesson-guide.md#worked-day-16)

| Day and question | Starting view | Experiment | Evidence to look for |
| --- | --- | --- | --- |
| **16 · Which reference moves?** | Benchmarks and bands · Monthly retail | Keep the benchmark at 60 and the mean line enabled. Filter Revenue to `gte` 50. Add a median as an independent check. | Nine rows remain. The benchmark stays at 60. The mean moves from about 65.08 to 71.78 and the filtered median is 68. The option tells ECharts how to compute the statistic. |
| **17 · What is a date interval attached to?** | Benchmarks and bands · Monthly retail, full year | Extend the Apr–Jun band through Jul and rename it “Review window”. Mark the maximum. Swap axes and find the new coordinates. | The band follows Month onto the category Y axis. The peak is December at 98. The label accurately describes the extended period. |
| **18 · Which points fitted this line?** | Linear fit · Regional channels | Inspect the fitted endpoints. Filter Stores to `gte` 60, then `gte` 81. Track both series’ dataset indices. | Three qualifying pairs fit a line from Stores 61 to 81. The fit uses a separate two-row DataFrame. With one distinct X remaining, Studio omits the fit and explains why. |
| **19 · When does a moving average begin?** | Moving average · Monthly retail | Predict the first complete three- and four-observation windows. Change the window. Repeat with Weather log, High, window 3. | The first retail values are 45 in March and 48.25 in April, respectively. After the weather gap, a complete three-observation mean returns on 26 April. |
| **20 · Audit a claim** | Choose Benchmarks and bands, Moving average, or Linear fit | State a claim, identify its contributing rows, then choose one change that could alter your interpretation. Hand the reader enough evidence to check it. | The learner distinguishes an observed value from a fixed reference or estimate, identifies the calculation and population, and reports the result of the changed case. |

## Days 21–25 · Interaction and the canvas

Use real reader tasks such as identifying a point, comparing June across panels, and reading the chart on a small screen. Introduce an interaction by asking what changes for the reader, what happens to the rows, and where that choice is recorded.

| Day and question | Starting view | Experiment | Evidence to look for |
| --- | --- | --- | --- |
| **21 · What should a reader learn on hover?** | Scatter plot · Regional channels | Choose Region, Wholesale, then Online in tooltip display order. Bind direct labels to Region and test overlap handling at two widths. | Pacific Northwest can be identified with Wholesale 20 and Online 48. `encode.tooltip` records the order, `label.formatter` the field, and `labelLayout` the overlap policy. |
| **22 · Are these regions highlighted, outside the window, or filtered out?** | Scatter plot · Regional channels, sort by Stores to expose the inspector, enable brush and toolbox | Try a brush, clear it, use toolbox zoom and restore, then apply Stores `gte` 60. Check the source and plotted tables between actions. | Brushing changes mark emphasis. Zoom changes the visible range and can affect ECharts’ internal data processing. The authored dataset filter is the operation that takes the Studio plotted-row table from six to three. |
| **23 · Do these two Junes refer to the same thing?** | Linked panels · Monthly retail | Compare June across panels, disable pointer linking, then restore it. Trace each series to its axes and grid. | Revenue is 56 and Target is 60. Separate value scales are compatible with a shared Month pointer. The control lives under grid in Studio and emits root `axisPointer.link`. |
| **24 · Who owns this patch of colour?** | Linked panels · Monthly retail, enable graphic and toolbox | Set a canvas background, then enable `grid.show` and set the plot background. Pin a source note in `graphic` and test a zoom. | The outer margin and plot interiors can differ. The note has canvas coordinates. A data-bound `markArea` would need axis coordinates. Identify which one best fits a source credit. |
| **25 · Does the comparison survive a narrow screen?** | Responsive layout · Monthly retail | On a wide enough screen, test rendered chart widths of 560 and 480 px. Describe the layout change and add a meaningful `aria.label.description` and a redundant visual cue. | At widths ≤ 500 px the legend moves below and the right grid inset becomes 8%. Above it, the inset is 24% and the legend is vertical. A reader can recover a named comparison from text or data and still distinguish the series. |

## Days 26–30 · Independent reading, building, and revision

Give a brief before naming any option path. The gallery and reference become working tools. Use the builder for the reconstruction, capstone, and final unplanned change. The section has a solo route as well as a peer walkthrough.

| Day and question | Starting view | Experiment | Evidence to look for |
| --- | --- | --- | --- |
| **26 · What is portable from an unfamiliar example?** | Apache’s *Bar with Background*, then Bar chart · Monthly retail | Read the gallery option and predict the effect of the bar-track property. Recreate that behaviour in Studio using Revenue. [Gallery example](https://echarts.apache.org/examples/en/editor.html?c=bar-background) | The chart shows bar tracks through `series[0].showBackground`. March still maps to 45 through the DataFrame. Explain the difference between the gallery’s arrays and Studio’s named bindings. |
| **27 · Can you learn one property from the reference?** | Stacked bars · Regional channels | Pick one supported property you have not used. Find its parent, permitted value, default or inheritance rule, and a way to reveal its effect. `legend.itemGap` is a fallback. | Supply a reference link, a prediction, and the option before and after the edit. Explain what happens on reset. A change in legend spacing should leave channel totals intact. |
| **28 · What does the reader need to decide?** | A clean named starter and one bundled sample of your choice | Choose a [capstone brief](assessment.md#capstone-briefs). Write the intended comparison, grain, bindings, and one interaction. Build a first view. | A second person, or the learner working from their own notes, can trace one visible mark to a row. The chart offers a specific answer to the brief. |
| **29 · Where does your design stop working?** | Day 28 view, reopened from its note if needed | Test a narrow layout and an analytical edge case such as an empty subset, a missing reading, or a cutoff equal to an observation. Revise the chart or qualify its claim. | Record the starting conditions, predicted failure, observed evidence, and repair. Distinguish a layout limitation from an error in the data or option. |
| **30 · Can you teach it back and change it?** | Revised capstone | Give a short walkthrough from source to option to decision. A peer chooses a fresh change, or draw a different variation from the assessment guide. Predict, edit, verify. | The learner identifies the owning path, handles the change, and justifies the result with a value or invariant. Use the [rubric](assessment.md#capstone-rubric) to give specific feedback. |

A learner who finishes early can test a second field, fine-tune the spacing of a bar group, or make a benchmark identifiable in a different palette. The field guide has four design exercises for learners who want more precise control. [Fine-tuning challenges](studio-reference.md#fine-tuning-challenges-for-experienced-chartmakers)
