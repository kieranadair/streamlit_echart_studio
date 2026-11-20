# Delivery plan and decisions

**The course is in curriculum design.** The merged builder supplies the chart workbench. The reference set defines the learner promise, thirty proposed experiments, known-answer data, worked lesson designs, and a way to test learning. The course itself is awaiting a learner pilot and production authoring. Begin future work at the [course charter](README.md).

## What is settled and what is proposed

| Status | Decision and rationale | When to revisit |
| --- | --- | --- |
| Project goal | Teach Apache ECharts through the existing chart builder to people already proficient with Tableau and visualisation. Use official option names and meaningful visual changes. | Revisit if the intended audience or primary teaching mechanism changes. |
| Existing product choice | Keep the native Streamlit ECharts renderer, a DataFrame-backed dataset, editable defaults and hierarchy, and a readable option beside the learning workflow. | Recheck property names and defaults when the renderer or Studio version changes. |
| Project priority | Emphasise fine control over charts and canvas, with a few teaching datasets. Export and uploads have low priority. | Revisit when an actual learning objective depends on a different data source or representation. |
| Curriculum proposal | Six sections of five days. End each section with reconstruction, diagnosis, or transfer. Calibrate depth from the solo learner’s actual sessions. | Use observed completion time, hint use, and the ability to handle a changed case. |
| Curriculum proposal | Offer exact starts and layered hints early, then withdraw them. Keep the free explorer available during the course. | Revisit if beginners lose their place or experienced learners find the route too prescriptive. |
| Data proposal | Keep all core days runnable on bundled samples. Introduce Palmer Penguins first for transfer. Consider airline passengers for a seasonal window exercise. | Check compatibility with each starter, educational value, attribution, and the airline CSV’s redistribution basis. [Data decisions](datasets.md) |
| Assessment proposal | Use a source-to-option walkthrough and an unplanned change. Allow a peer or solo route. | Calibrate the rubric using pilot work. A technically different solution can meet the same reader brief. |

## From design to release

| Stage | Work and dependencies | Output and evidence for moving on |
| --- | --- | --- |
| **1 · Rehearse the first investigations** | Kieran walks through days 1 and 16 using the [worked lessons](lesson-guide.md) and try the [pilot cards for days 8 and 25](assessment.md#two-short-pilot-cards). Use the current app and lesson notes. | Four reproducible starts, an expected result for each, and a list of controls or concepts that need clearer wording. Kieran can reconstruct the baseline on a later attempt. |
| **2 · Pilot the teaching method** | Run the [solo pilot](assessment.md#pilot-design) with Kieran. Observe prediction, navigation, checking, and independent variation. | A short findings note, revised exemplar, and a decision about which recurring friction, if any, warrants a builder change. |
| **3 · Author in five-day sections** | Produce learner-facing material from the syllabus and template. For each section write the checkpoint first, then its four preparatory investigations. Give every day an example, dataset, explicit starting edits, and a changed case. | Thirty lesson drafts and six checkpoints. A fresh-session walkthrough checks the option, chart, and relevant rows for every core day. A second reviewer follows at least the checkpoint of each section using only the learner material. |
| **4 · Connect the course to Studio** | Use the existing renderer, option compiler, data preview, and explorer. Provide a way to open a day, see its prompt, reveal hints, and recover its starting view. A named starter plus a short recipe is the minimum viable route. Decide on deep links and one-click starts from pilot evidence. | A learner entering at day 16 can obtain the twelve-month baseline and make the first prediction. A learner on day 25 can still reach the ordinary chart controls. Reopening a lesson gives a clear way to distinguish its suggested start from the learner’s edits. |
| **5 · Review the complete journey** | Try the sequence in order and enter selected days directly. Check keyboard and text routes, chart widths, empty or missing data, and option paths against the actual renderer. Try the final brief with a learner who has used the earlier sections. | An end-to-end walkthrough, documented accessibility findings, a verified capstone variation, and resolved or clearly identified lesson-specific issues. Test the chosen hosted deployment using a fresh session. |
| **6 · Publish and maintain** | Link the course entry point from the project. Keep each day independently addressable in the chosen delivery format and let learners reach the source materials. Retest affected days as Studio evolves. | A dated course release tied to a builder revision. Each future revision can identify the affected day, the evidence, and the source in one place. |

**The smallest useful course surface** is a reader brief near the working chart, a visible way to choose or restore the intended starting state, and optional hints and checks. Long source essays belong in the reference material. Writing a second chart renderer, thirty standalone demo apps, or a progress-account system would add maintenance without establishing that the learner understands the option. Keep those decisions outside the first pilot.

## Questions the pilot can answer

| Question | Working choice | Evidence that would change it |
| --- | --- | --- |
| How much prompting do learners need to inspect the option? | Ask for a specific path or a row on each day. | Learners can complete the actions but repeatedly fail to explain a new case. Try an earlier option-reading prompt. |
| Do learners need a dedicated “Start this day” action? | Supply a named starter and recipe in the paper pilot. | Returning learners repeatedly work from stale edits, or two authors cannot reproduce the same start from the recipe. |
| How much of the final work should involve code? | Require option reading, tracing, and adaptation in the builder. Offer handwritten fragments or a code-based extension as enrichment. | Graduates can use the UI but cannot explain a property in a short unfamiliar option. Increase reference-reading and reconstruction practice. |
| Would a larger dataset improve learning? | Pilot the three small samples first. | Brushing six points is mechanically clear but gives learners little reason to select. Try the proposed penguin scatter task and compare explanations. |
| Can people read the result through different means? | Supply a value, field name, and relevant option alongside a visual judgment. | Keyboard or assistive-technology testing identifies an unreachable control or evidence available only by gesture. Provide an alternative task route and record the product gap. |

## Picking this up in a future session

1. Read the charter, find the day or capability in the syllabus, and inspect the current version of the builder. The initial curriculum baseline is [revision 626bf89](https://github.com/kieranadair/streamlit_echart_studio/tree/626bf892b02642785cd2af13c411529ef29e5f45).
2. Use [Studio behaviour](studio-reference.md) and [checked values](datasets.md) to reproduce the intended evidence. Verify an unfamiliar option against Apache’s reference and the bundled runtime.
3. If a feature is proposed, record the learner question, the affected day, what the current builder already permits, and what evidence would improve. If a dataset changes, revisit every dependent answer key.
4. When pilot evidence changes a decision, update the corresponding row above, record the reason and revision, and update the syllabus or lesson that depends on it. Keep one canonical lesson sequence in [syllabus.md](syllabus.md).

**Next milestone.** Rehearse the worked lessons and the day 8 and day 25 pilot cards with Kieran. Use what they can explain on the changed case to decide which course affordances and hints deserve development.
