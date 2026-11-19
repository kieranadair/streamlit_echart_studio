# Assessment and pilot

The learner’s evidence is a working chart, an explanation that connects it to data, and a successful change under new conditions. Screenshots are useful for discussing appearance. The option fragment and a check against a row or calculation establish how the result was produced. The assessment works in a conversation, in a learner’s notes, or during an observed session.

## Six checkpoints

| Day | Ask for | A variation that distinguishes understanding from imitation |
| --- | --- | --- |
| 5 | A two-series comparison and a trace from one mark to its row | Reverse which measure is a line. Ask whether either measure’s source values should change. |
| 10 | A ranking explained in both table order and screen order | Ask for Stores above 61 after the learner has shown at least 61. Ask them to name the disappearing region before they edit. |
| 15 | A defensible encoding choice and an explanation of a colour boundary | Give the value exactly equal to the cutoff. Ask the learner to move the boundary and identify a second value whose colour should stay the same. |
| 20 | An analytical claim plus its population, units, and calculation | Change the filter field while preserving the plotted measure. Ask *which observations* now inform the claim. |
| 25 | A readable comparison at two widths, a text equivalent, and an explanation of layout ownership | Give a narrow chart in a wide browser. Ask which width controls `media.query` and how to test the answer. |
| 30 | A chart built from a reader brief, a trace to source, and a live or independently recorded revision | Use a change the learner has yet to try. The learner can consult the official docs, predict the effect, and verify what happened. |

A useful feedback sentence is “You correctly located the filter. Now show which series actually reads its output.” It tells the learner exactly which link in the explanation to strengthen.

## Capstone briefs

Give the learner the **brief** on day 28. Keep the variation for the day 30 walkthrough. If working solo, choose a variation only after recording the initial claim. A learner can propose their own brief using the same evidence requirements.

| Brief | What an adequate solution lets a reader do | Possible change to request |
| --- | --- | --- |
| **Retail review.** A manager wants to know when revenue fell short of target and how a benchmark changes the interpretation. | Compare actual and target for the same month. Name at least one shortfall in thousands of dollars and trace both marks. A threshold, an interval, or a narrative annotation can be justified. | Restrict the report to months meeting a target threshold. Predict which rows survive and whether a fixed benchmark moves. Or ask for a layout that still communicates the March shortfall at 480 px. |
| **Regional sales.** A channel lead wants to judge whether a region’s apparent strength comes from one channel or its mix. | Answer a named comparison, specify whether values are individual channel amounts or sums, and defend a stacked bar, scatter plot, or heatmap for that question. For Pacific Northwest the channel amounts are 61, 48, and 20. | Change the qualification rule from at least 61 to strictly above 61 in Stores, or change the cut between two sales bands. Ask which region or cell changes and why. |
| **Weather briefing.** A reader wants to distinguish daily variation, a smoothed pattern, and a period without High readings. | Identify the date grain, express temperatures in °C, and explain how missing readings are represented. A second measure, a rolling window, or two linked panels are possible design choices. | Change the window length or compare with Low. Ask when a complete estimate becomes available and which apparent visual continuity comes from a display setting. |

For all three, a credible answer can qualify a claim. Six regional observations can illustrate a relationship. A line fitted to those observations cannot establish its cause. A line spanning a missing interval says nothing by itself about unobserved temperatures.

## Capstone rubric

Use these anchors during the pilot. A reference lookup is normal professional work and is compatible with an independent score.

| Dimension | 0 · Evidence still needed | 1 · With a hint | 2 · Independently demonstrated |
| --- | --- | --- | --- |
| Data lineage | The chosen row, field, unit, or population conflicts with the claim. | Locates the appropriate row or derived table after a prompt. | Traces a named mark to an observation or calculation, with correct units and contributing rows. |
| ECharts ownership | Can describe the appearance only. | Identifies a branch after guidance and recognises its path. | Identifies the actual series, component, binding, or default that produces the behaviour. |
| Prediction and revision | A change is made without checking the outcome. | Revises the view and validates it after a suggestion. | Predicts a novel change, makes it, and uses evidence to confirm or correct the prediction. Explains an unexpected result. |
| Fit to the reader | The reader cannot answer the stated question from the offered evidence. | Supplies a working comparison or text equivalent after prompting. | Makes the intended comparison legible and supplies a second way to read it under a relevant constraint. |
| Reference use | Repeats a property name without locating its context. | Finds the relevant example or reference entry with guidance. | Uses a reference to resolve a concrete uncertainty, then tests the interpretation in Studio. |

Record the five dimensions separately. A proposed sign of readiness is independent performance in lineage, ownership, and revision, plus evidence for the remaining dimensions. Return one specific improvement and a changed case to try. The pilot can reveal whether the anchors need adjusting.

## Pilot design

**Participants and scope.** Invite three to five Tableau-proficient people who can explain an existing visualisation and are new to authoring ECharts options. Aim for some variation in coding experience, screen size, and input method. This is a proposed small qualitative pilot. Technical rehearsal has checked the builder and its data. Testing with learners is a later milestone.

**Session A, approximately 35–45 minutes.** Start with day 1 and a changed month. Then supply day 8’s ranked starting view and ask the learner to predict and check a filter. Observe whether the data preview and option readout help them recover from a wrong prediction. Let them try unaided before offering the first hint.

**Session B, several days later, approximately 30–40 minutes.** Start with five minutes of reconstruction from the retail or ranking brief. Give half the group day 16 and the others day 25, providing the starting recipe for the skipped days. Finish with one previously unseen condition. This tests lesson design and retention of the early skill. A later ordered pilot covers all six sections and the capstone.

### Two short pilot cards

Use the [worked lessons](lesson-guide.md) for days 1 and 16. These companion cards supply the other two starting views.

**Day 8 · Qualifying regions.** Open **Rank the regions** with Regional channels, descending Stores, and an empty filter. Tell the learner, “The manager will review regions with store sales of at least $60,000. How many bars do you expect, which region should be highest, and how would you check that the source still has six regions?” Give the learner time to experiment. If needed, point first to **dataset**, then to the filter dimension, operator, and value. After the check, ask for *above $61,000*.

**Observer key.** Stores is recorded in thousands. The first condition is `gte 60`, which retains 81, 67, and 61. The changed condition is `gt 61`, which retains 81 and 67. Observe whether the learner can explain the distinction between input rows and the series’ transformed dataset without relying on the visible number of bars.

**Day 25 · A narrow report.** Open **Responsive layout** with Monthly retail on a screen where the chart column can exceed 500 px. Tell the learner, “A colleague opens the same report in a smaller panel. Which part of the chart should move, what sales comparison must survive, and how could you check the boundary?” Let them resize with **Preview size**. If needed, point to the **media** tab and the two options in the readout. Ask for a short chart description that would help a reader identify June’s shortfall.

**Observer key.** Try 560, 500, then 480 px in the chart. The rule is inclusive at 500. At the two smaller widths the legend is horizontal and the right inset is 8%. Above the breakpoint the legend is vertical with a 24% inset. June Revenue 56 and Target 60 have the same meaning at all widths. If both previews are already clamped to a narrow column, inspect the rule and move to a wider viewport for the physical crossing. Note whether the learner discovers that distinction.

**Technical rehearsal at builder revision 626bf89.** A Chromium walkthrough of the running local app reproduced the March pair of 45 and 49, the three qualifying regions and subsequent strict two-region subset, the filtered mean of 71.78 and median of 68, and the narrow layout at exactly 500 px. Switching the filter field to Target and then entering 60 yielded the predicted mean Revenue of 75.14. The chart restored the wide layout at 560 px. These checks establish known working examples for the facilitator. Learner reasoning, timing, and assistive-technology usability are the questions for the pilot.

### Capturing and using pilot evidence

**Observation sheet.** One row per task is sufficient. Collect notes with the participant’s agreement. Ordinary author notes can answer the pilot questions without a new analytics system.

| Day and starting state | Prediction in the learner’s words | First edit and evidence inspected | Highest hint used | Result on the changed case | Time, access issue, or ambiguity | Proposed revision |
| --- | --- | --- | --- | --- | --- | --- |
| Example · 8, ranked regional bars | “Turning the axis over will reverse the table.” | Toggled inverse and inspected the table | Concept hint | Correctly used a sort on the next attempt | Found the inspector after prompting | Mention both check surfaces in the prompt |

**How to act on observations.**

- A disagreement between the answer key and the actual option or data calls for a technical correction and a replay of that example.
- Two learners encountering the same navigation problem is a reason to revise the starting recipe or prompt and try it again. Consider a builder affordance when the friction persists with a clear recipe.
- If learners reproduce the demonstrated steps but fail the changed case, introduce a contrasting case or a self-explanation prompt. More controls on the page are unlikely to solve that learning problem.
- Check the keyboard path to selectors, option text, and data tables. For hover or brush tasks, offer a text/data investigation of the same question and a companion demonstration of the gesture. Record which interactions were actually tested with assistive technology.
- Report counts as counts, together with examples of learner reasoning. Use repeated independent explanations over the full course to judge the final outcome. Completion clicks alone measure navigation.

**Pilot deliverable.** A short note listing the three most consequential findings, their evidence, the lessons affected, and the changes worth retesting. Carry decisions into the [delivery plan](delivery-plan.md), and keep personal participant details out of the public course documents.
