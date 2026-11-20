# 30-day syllabus

**Audience and outcome.** You already know how to choose and critique a visualisation. Over thirty sessions, learn to express that judgment in Apache ECharts, investigate a surprising rendering, and hand a colleague a chart they can revise from its option.

**How to use a day.** Allow about 30 active minutes. Take four minutes to read the parameters, inspect the complete intended view and its source, and make a prediction. Work through three challenges in Studio (roughly seven, seven and eight minutes). Before each edit, predict a specific consequence. After each edit, inspect the chart and the relevant row or option path and explain what happened. Use the last four minutes to hand over your evidence. Times are design estimates for Kieran’s solo pilot. Each numbered task below is core work.

Choose the named example and dataset in **Starting example** and **Dataset**. A fresh session restores the published starts. When a day uses a previous result, its brief names the settings needed to rebuild it. The [lesson guide](lesson-guide.md) gives the seven-part authoring sequence. The [dataset guide](datasets.md) gives units, known answers and optional transfer sources.

## Days 1–5 · Build and audit the option behind a comparison

### 01 · Audit a monthly performance review

**Start in Studio.** Bar chart · Monthly retail. **Read in the option.** `dataset.source`, axis types, `series.encode`, `series.type`, `tooltip`, sort transform.

1. Build the actual-versus-target view. Reconcile an annual surplus with monthly shortfalls and trace both March marks to one row.
2. Compare item and axis inspection. Change tooltip order and identify two months that put different series first.
3. Rank months by Revenue, trace both series to the derived table, and repair the reading of a line that now connects months out of calendar order.

**Hand over your evidence.** Give Finance an annual answer and Operations a month to investigate. Restore the chronological view and explain its contract. [Full lesson and checks](day-01.md)

### 02 · Choose a grain for a channel review

**Start in Studio.** Bar chart · Regional channels. **Read in the option.** wide source, per-series encoding, long source, `encode.value`.

1. Build a three-channel comparison from the six-row table. Count source rows, series and marks. Reconcile Pacific Northwest’s three values with one source row.
2. Switch to Heatmap with the same sample. Predict the new grain before inspecting the preview. Trace the Online cell through Region, Channel and Sales. Compare how each option identifies “Online.”
3. Answer two briefs, “compare channel mix within a region” and “find large values across regions.” Choose a view for each and point to the additional computation a reader needs to recover a regional total.

**Hand over your evidence.** Diagram the same 48 in both contracts. Account for six wide observations and eighteen cells. Explain why a series count alone cannot establish the grain.

### 03 · Test whether a horizontal distance means elapsed time

**Start in Studio.** Bar chart · Weather log, High as a line. **Read in the option.** `encode.x`, axis type, filter dimension, category spacing.

1. Compare Date and Day as X bindings. Read both emitted axis types. Trace day 1 to 1 April and 17 °C. Explain why two equally spaced plots can encode different quantities.
2. Filter on High so the surviving dates have an interruption (try High ≥ 18). Compare the dates of two successive surviving observations. Switch the Date axis between time and category and inspect their separation.
3. Restore the full source, then investigate 20–23 April on the time axis. Distinguish a row excluded by the filter from a retained day with a missing High. Use Low to check that the station still has rows.

**Hand over your evidence.** Defend an axis for reporting elapsed time. Give a pair of dates, their elapsed days and the path responsible for their spacing.

### 04 · Establish a typography hierarchy and audit its defaults

**Start in Studio.** Bar chart · Monthly retail. **Read in the option.** root `textStyle`, title and subtext styles, `xAxis.axisLabel.rotate`, grid.

1. Build a title/subtitle that identifies the decision and carries the units. Change the chart-level font family, then adjust only the title’s font weight. Compare the scope of each edit. Locate both owners.
2. At a narrow preview width, try rotation, then restore it and try a grid inset. Compare which change affects the labels, plot rectangle and space available for bars.
3. Reset one leaf, disable its parent, then re-enable it. Inspect the option after each action. Distinguish an omitted renderer default, an inherited value and a stored explicit choice.

**Hand over your evidence.** Provide the smallest set of overrides you would keep, their paths and a readable narrow view. Demonstrate how to recover the baseline.

### 05 · Deliver a comparison to a different stakeholder

**Start in Studio.** Bar chart · Weather log, Date and High. **Read in the option.** shared scale, two series, tooltip, line and label styles.

1. Build a daily range comparison using High and Low on a common scale. Choose the marks and verify both values for 1 April.
2. A reader wants to identify either series without colour. Design a redundant cue, change the palette and check the same date and the missing interval.
3. Switch from an overview to an inspection task. Configure a tooltip for a named date and compare it with the direct labels or legend. Rebuild the crucial settings from a short handover note.

**Hand over your evidence.** Trace the 1 April high (17 °C) and low (11 °C). Explain which edit changed the reader’s access to a measurement and where the chart signals missing evidence.

## Days 6–10 · Coordinates, order and data pipelines

### 06 · Transpose a ranking without losing its meaning

**Start in Studio.** Bar chart · Regional channels, Stores and Online. **Read in the option.** `encode.x/y`, axis types, grid inset.

1. Build a two-channel regional comparison. Predict both series’ coordinates after **Swap X and Y**. Test Pacific Northwest before and after.
2. Tune a horizontal layout for the longest region names at two preview widths. Compare a grid inset with a label treatment and document the trade-off in plotting space.
3. A colleague wants the order reversed with the amounts still on X. Reverse only the category axis, then compare its option to the earlier transposition.

**Hand over your evidence.** Trace 61 and 48 across both orientations. Identify one setting that changes reading direction, one that changes field assignment and one that changes available space.

### 07 · Reconstruct two visually identical rankings

**Start in Studio.** Rank the regions · Regional channels. **Read in the option.** sort dimension/order, `yAxis.inverse`, series binding.

1. Predict the first plotted row and top bar for descending Stores with each axis direction. Test both.
2. Make the same largest-first display with ascending sort and the opposite axis direction. Use the inspector to distinguish the two charts without looking at the option.
3. Restore the descending-table solution. Rank regions by Online while drawing Stores. Find the pair whose relative order reverses and decide whether the title needs to name both fields.

**Hand over your evidence.** Give a two-row diagnostic for a hidden sort error. Southern Highlands and Northern Coast trade places when Online supplies the order.

### 08 · Specify, audit and revise an eligibility pipeline

**Start in Studio.** Rank the regions · Regional channels. **Read in the option.** `fromDatasetIndex`, `transform.config`, `datasetIndex`, `encode`.

1. Implement a threshold with a record exactly on the boundary. Predict the strict subset and diagnose an empty result from both tables.
2. Produce matching screen rankings with different plotted table orders. Follow the series’ dataset index to prove which pipeline the director received.
3. Change to a cross-channel brief. Separate eligibility, rank and length and devise a test that would expose an accidental sort on the displayed measure.

**Hand over your evidence.** Write a three-clause data specification and supply a witness row or pair for each clause. [Full lesson and checks](day-08.md)

### 09 · Audit a chart with two horizontal axes

**Start in Studio.** Bar chart · Weather log, High and Low on Date. **Read in the option.** per-series X field, `xAxisIndex`, time/value axes.

1. Assign Low to Day while High stays on Date. Draw the series-to-axis map and verify 1 April on both axes.
2. Change only Low’s binding back to Date. Predict how the axis array and indices will simplify. Inspect the option and explain why the two series can share a scale now.
3. Compare the mixed-axis version with a shared-Date view across the missing High interval. Decide which you would ship to a reader comparing readings at the same time.

**Hand over your evidence.** Supply both option fragments and a precise condition under which separate scales would be justified.

### 10 · Accept or reject a regional shortlist

**Start in Studio.** Rank the regions · Regional channels. **Read in the option.** filter, sort, axis direction, encoded measure.

1. Build an acceptance test for “Stores at least 61, ranked descending.” Predict first row, top bar, boundary row and row count. Run it.
2. Construct a plausible wrong answer by pairing ascending sort with an axis reversal. Diagnose it under a brief that also requires the plotted table in descending order.
3. Change the brief to “Online at least 39, largest Stores first.” Confirm the exact-boundary region, then show how to distinguish ranking by Stores from ranking by Online on this subset or a deliberately widened subset.

**Hand over your evidence.** Deliver the option paths and the smallest set of row checks that would catch an incorrect threshold, sort or display direction.

## Days 11–15 · Control the visual encoding

### 11 · Separate part-to-whole and side-by-side comparisons

**Start in Studio.** Stacked bars · Regional channels. **Read in the option.** `stack`, `barGap`, `barCategoryGap`, legend selection.

1. Reconcile one full stack with its three source amounts. Move Wholesale outside the stack and explain both resulting endpoints.
2. On the last bar series, vary within-group and between-category gaps separately. Capture the two paths and design spacing for comparing the pair across regions.
3. Hide one channel with the legend, then compare that reading with editing the stack assignment. Identify which behaviour a reader can reverse on the chart.

**Hand over your evidence.** Give Pacific Northwest’s full total (129), remaining two-channel subtotal (109) and separate Wholesale amount (20). Defend the layout for a channel manager.

### 12 · Communicate a gap without implying a measurement

**Start in Studio.** Area chart · Weather log, High. **Read in the option.** `connectNulls`, `areaStyle`, `showSymbol`, `smooth`.

1. Locate the final observation before the gap and the first after it. Compare a broken line with a bridge and write the interpretation each invites.
2. Vary fill, symbols and smoothing one at a time. Identify a styling choice that makes the distinction between observation and interpolation easier to see.
3. Add Low and choose a design for a reader deciding whether the station stopped reporting. Inspect both series on the missing dates and write a caption that the source supports.

**Hand over your evidence.** Name the interval (20–23 April), the field with missing values and the properties responsible for apparent continuity. Give a reason for keeping or dropping the fill.

### 13 · Commission a bubble scale

**Start in Studio.** Scatter plot · Regional channels, Stores on X and Online on Y. **Read in the option.** `visualMap.dimension`, `seriesIndex`, `inRange.symbolSize`, `symbolSize`.

1. Label or identify two points from their rows. Map Wholesale to size and trace a point through all three encodings.
2. Configure two different diameter ranges using the same field. Compare how strongly they suggest differences and explain what someone could infer from the area of a circle.
3. Try fixed sizes with numeric Wholesale in the tooltip. Choose a version for spotting the largest wholesale market and another for reading an exact amount.

**Hand over your evidence.** Explain why Eastern Seaboard can change apparent prominence while staying at (81, 57). Give its Wholesale value and the path that owns each change.

### 14 · Make heatmap colour comparable across views

**Start in Studio.** Heatmap · Regional channels. **Read in the option.** `encode.value`, `visualMap.dimension`, `min/max`, `inRange.color`.

1. Trace Pacific Northwest × Online from its long row through both axes to colour. Transpose the chart and recover that same cell.
2. Set two different continuous domains around the same sales values. Explain how the same 48 can receive a different shade and how you would compare two screenshots fairly.
3. Filter to one Channel, then compare a fixed common domain with one tuned for the subset. Choose which question each version answers better.

**Hand over your evidence.** Deliver the domain, units, source grain and a check showing that the identified value survives the redesign.

### 15 · Write a defensible classification rule

**Start in Studio.** Heatmap · Regional channels. **Read in the option.** continuous vs piecewise visual map, `pieces`, boundaries, labels.

1. Propose three operational sales bands. Translate one prose definition into exact inclusive and exclusive bounds. Test an observed value at the cutoff.
2. Put the first upper cutoff at 39, then move it to 38. Verify Northern Coast × Online and Western Plains × Stores. Identify one changed and one unchanged classification.
3. Reconstruct a continuous alternative and compare how each answers “which region is slightly ahead?” versus “which needs review?” Choose the version to publish with a meaningful legend.

**Hand over your evidence.** Provide a boundary test and a defensible reader brief. A band label must accurately describe the rule it executes.

## Days 16–20 · References, calculations and their populations

### 16 · Audit a benchmark, a mean and a median

**Start in Studio.** Benchmarks and bands · Monthly retail. **Read in the option.** `markLine.data`, `valueDim`, filter transform, `datasetIndex`.

1. Reconstruct the full-year mean and compare the rule for that line with the coordinate of the fixed benchmark.
2. Filter Revenue ≥ 50. Predict both reference positions, verify the mean and add an independently checked median. Explain which population each line describes.
3. Filter on Target ≥ 60 while continuing to average Revenue. Decide which line answers the manager’s revised question and prove it with a numerator and denominator.

**Hand over your evidence.** Deliver a population statement for each chart and an option fragment distinguishing fixed and computed references. [Worked paths and checks](lesson-guide.md#worked-day-16)

### 17 · Attach an annotation to the right coordinate system

**Start in Studio.** Benchmarks and bands · Monthly retail, full year. **Read in the option.** `markArea`, `markPoint`, axis coordinates, `graphic`.

1. Extend the Apr–Jun band through July. Rename it and inspect its two endpoints. Explain why a Q2 label would now mislead.
2. Mark the maximum and transpose the chart. Trace both band endpoints and December’s peak through the new coordinates.
3. Add a fixed source credit using graphic. Resize the chart and contrast its anchoring with the band and peak. Choose an owner for a note about July specifically.

**Hand over your evidence.** Supply the coordinates for one interval and one observation, and explain which annotation should follow a change in the plotted maximum.

### 18 · Audit a fitted line as the sample shrinks

**Start in Studio.** Linear fit · Regional channels. **Read in the option.** native filter, derived fit DataFrame, series dataset indices and encodings.

1. Trace the six observed pairs and two fitted endpoints to their respective datasets. Distinguish the predicted Y at an endpoint from a measured Online amount.
2. Filter Stores ≥ 60. Inspect the three surviving pairs and recompute a prediction using the two fitted endpoints. State the observed X range over which you would show the fit.
3. Retain only Stores ≥ 81, diagnose the missing fit from the data, then recover it. Explain why one distinct X makes slope unidentifiable.

**Hand over your evidence.** Hand over the observed-versus-fitted dataset map before and after filtering, with one limitation on the inference.

### 19 · Specify a rolling calculation precisely

**Start in Studio.** Moving average · Monthly retail. **Read in the option.** source order, plotted order, derived trend dataset and window length.

1. Work out the first complete three- and four-observation estimates by hand. Change the window and locate those rows in the derived table.
2. Sort the displayed observations by Revenue. Inspect the trend table’s dimension order and distinguish the calculation order from the visible sequence. Choose a display safe for a time trend.
3. Transfer a three-observation window to Weather log, High. Predict the last missing estimate after the gap and the first date with a complete new window.

**Hand over your evidence.** Give the calculation specification, including how the window handles missing readings, and cite March 45, April 48.25 and the 26 April recovery.

### 20 · Challenge an analytical claim with a competing explanation

**Start in Studio.** Monthly retail, using Benchmarks and bands and Moving average. **Read in the option.** reference rules, transform population, derived trend.

1. Build the case that June underperformed against its own target. Trace 56 and 60 and distinguish that target from a constant benchmark at the same height.
2. Give June a second comparator using a three-month trailing Revenue mean. Compute the value independently and identify which observations inform each comparison.
3. Restrict the benchmark report to months with Revenue ≥ 60. Diagnose what happens to the June claim under that selection and choose the appropriate population for the manager.

**Hand over your evidence.** Provide two qualified claims, their calculations and a condition under which June can disappear from the evidence. Explain why a changing population deserves an explicit label.

## Days 21–25 · Design interaction, panels and canvas together

### 21 · Make point identity recoverable at two sizes

**Start in Studio.** Scatter plot · Regional channels. **Read in the option.** `encode.itemName`, `encode.tooltip`, label formatter and layout.

1. Design an identification tooltip with Region, Wholesale and Online in a deliberate order. Verify Pacific Northwest’s 20 and 48 from the source.
2. Bind direct labels to Region and narrow the chart. Compare overlap handling and marker size. Explain what information a hidden label costs.
3. Produce a version for a static screenshot and a version for pointer inspection. Test both on the same two named points and write a text equivalent for one comparison.

**Hand over your evidence.** Give one series fragment for field identity and one for presentation. Show how the reader can recover an exact value in each delivery context.

### 22 · Distinguish selection, zoom and exclusion

**Start in Studio.** Scatter plot · Regional channels. Sort by Stores to expose the data inspector. Enable brush and toolbox.

1. Select a group with a brush. Predict whether source count, plotted count and mark emphasis will change. Check each and clear the selection.
2. Zoom to a similar-looking subset, then restore. Compare the option’s zoom configuration with the authored dataset and explain what the plotted inspector measures.
3. Author a Stores ≥ 60 filter and repeat the reader interactions. Decide which mechanism to use for an analyst exploring locally and for a shared report limited to eligible records.

**Hand over your evidence.** Give a three-row comparison of brush, zoom and transform. Record the effect on the visible chart, inspector count and the reader’s way back.

### 23 · Audit alignment across independent panels

**Start in Studio.** Linked panels · Monthly retail. **Read in the option.** grid and axis arrays, `gridIndex`, series axis indices, `axisPointer.link`.

1. Draw the path from each series to its axes and grid. Use June to show what is genuinely shared between the panels.
2. Disable and restore linking. Inspect both panels and explain what pointer synchronisation guarantees about matching months and what it guarantees about vertical scales.
3. Build a shared-axis comparison of the same measures in Bar chart. Decide which design supports comparing absolute gaps and which helps inspect each series’ pattern.

**Hand over your evidence.** Demonstrate June 56 versus 60 and defend a design for that question. Include the emitted root path for pointer linking.

### 24 · Design a canvas with three kinds of annotation

**Start in Studio.** Linked panels · Monthly retail, enable graphic and toolbox. **Read in the option.** root background, `grid.show`, grid background, `graphic.elements`, series annotations.

1. Give the margin and plot interiors distinguishable fills. Toggle grid visibility and inspect which setting owns each surface.
2. Pin a source credit to the canvas and mark a meaningful interval on a series. Zoom and change preview size. Record which coordinate system governs each.
3. Reduce the space available for the note. Reposition it or revise the insets, then check both panels and labels. Choose the smallest layout intervention that preserves the credit and comparison.

**Hand over your evidence.** Annotate a short option excerpt with the intended anchor for each element. Demonstrate one failure that would result from using the wrong anchor.

### 25 · Accept a responsive chart at its breakpoint

**Start in Studio.** Responsive layout · Monthly retail, chart column wider than 500 px. **Read in the option.** `baseOption`, `media.query`, legend/grid overrides, `aria.label.description`.

1. Compare actual chart widths 560, 500 and 480 px. Predict the exact-boundary result, then map the effective legend position and grid inset to base and override.
2. Identify a comparison that becomes harder to read on the narrow view. Revise a layout property and recheck on both sides of the breakpoint.
3. Write a description that communicates June’s shortfall and add a redundant visual distinction. Test whether the same quantities and series identities can be recovered from chart and text.

**Hand over your evidence.** Deliver three width checks and one reading check. Explain why a wide browser can still render the narrow rule in a Streamlit column.

## Days 26–30 · Read unfamiliar options and ship a defensible chart

### 26 · Port a gallery idea to a DataFrame contract

**Start in Studio.** Apache’s [Bar with Background](https://echarts.apache.org/examples/en/editor.html?c=bar-background), then Bar chart · Monthly retail. **Read in the option.** category arrays, series arrays, dataset encoding, `showBackground`, `backgroundStyle`.

1. Reverse-engineer the gallery’s rows and tracks. Identify the keys carrying values, the category labels and the visual treatment.
2. Reproduce the behaviour with Studio’s DataFrame, choose an appropriate track colour and verify March against its row. Explain which gallery keys the Studio bindings replace.
3. Add the changing Target measure. Test whether the uniform tracks could be mistaken for monthly targets. Choose a treatment and caption that distinguishes the two concepts.

**Hand over your evidence.** Supply a translation of the relevant paths and a screenshot or text description that explicitly identifies what a track means.

### 27 · Resolve an unfamiliar property from the reference

**Start in Studio.** Stacked bars · Regional channels. Choose an unfamiliar supported property. Fallback pair: `legend.itemGap` and `legend.padding`.

1. From the Apache reference, identify parent, accepted value, unit and default. State two plausible interpretations before editing the chosen property.
2. Design a minimal contrast to discriminate between them. For legend spacing, give the legend a visible background and change inner padding separately from inter-item spacing.
3. Carry the rule to a narrow chart. Reset the leaf and compare the option with the renderer’s effective appearance. Check a regional total to rule out a change to the data.

**Hand over your evidence.** Deliver a reproducible example and a reference link that another author can use to settle the same question.

### 28 · Prototype two answers to the capstone brief

**Start in Studio.** Choose a bundled sample and one [capstone brief](assessment.md#capstone-briefs).

1. Write a reader decision, source grain, units and one falsifiable acceptance check. Build a first chart and trace its most consequential mark.
2. Prototype a genuinely different solution in another starter using the same sample. Compare how each answers the named question and handles an exact-value lookup.
3. Pick one design. Add a purposeful interaction, then test it against a case where the competing prototype did better. State the remaining trade-off.

**Hand over your evidence.** Record the starter, dataset, essential options, evidence value and one reason you rejected the alternative. Use this note to reopen the chart tomorrow.

### 29 · Test the limits of the chosen design

**Start in Studio.** Day 28 view reopened from its handover. **Read in the option.** choose the layout, data-selection and encoding paths implicated by the brief.

1. Test a wide and a narrow chart. Predict what should survive and identify the first failure in labels, layout or inspection.
2. Stress-test the data claim using a boundary observation, an empty subset or a missing measurement. Compare the source and rendered evidence and isolate the owning option.
3. Repair the most consequential failure, repeat both tests and check the original baseline. Explain one limitation that still belongs in the published chart.

**Hand over your evidence.** Provide a before-and-after test record and a short recovery recipe. Name which claim the repair protects.

### 30 · Defend the chart and handle a change live

**Start in Studio.** Revised capstone with the original brief and a fresh session available. **Read in the option.** select the necessary paths independently.

1. Reconstruct the essential view from the day 28 note. Present a reader decision, a data trace and the minimal option excerpt that establishes its meaning.
2. Select an unused [capstone variation](assessment.md#capstone-briefs) after committing to your original claim. Predict which part should change, implement the request and verify against a source or derived row.
3. Challenge the revised result with a second viewing condition or population. Decide whether the original conclusion survives. Teach back the most surprising ECharts behaviour using one working example.

**Hand over your evidence.** Deliver the chart, its evidence, and a prediction for the next change. Score each dimension of the [capstone rubric](assessment.md#capstone-rubric) against something you actually demonstrated.
