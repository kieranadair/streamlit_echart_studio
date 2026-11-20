# 30 Days of Apache ECharts

A course design for people who already make charts in Tableau and want comparable control in Apache ECharts. **The learner’s workbench is ECharts Studio.** The learner moves between a source row, the rendered chart, and the ECharts option that connects them. This directory is the project’s curriculum reference. The proposed lessons are ready for author review and piloting.

## The promise

On day 1, reconcile an annual surplus with monthly misses, design a reliable hover comparison and diagnose a target line drawn in rank order. Each day targets about 30 minutes for an experienced visualisation practitioner, with three linked investigations and an independent handover. On day 30, give them an unfamiliar chart brief and a new constraint. They can choose the data grain, build a view, trace one mark through the option to its source, and predict and verify a revision. They can use the official reference when they meet a property the course has never shown them.

Keep four questions in view when designing or changing a lesson.

1. **What decision does the reader need to make?** The audience brings experience with marks, scales, comparisons, and dashboards. Give them a question worthy of that experience.
2. **What does one row represent?** Check a mark against a row or a calculation. Many convincing-looking errors begin here.
3. **Which part of the option owns the behaviour?** Use official names. Make the learner distinguish a data binding, a series setting, a chart-wide component, and a renderer default by observing their effects.
4. **Can the learner change the conditions and still explain the result?** A prediction, a purposeful edit, and a check on a different field reveal more than recreating a screenshot.

## Where to look

| If you are… | Start here |
| --- | --- |
| Deciding why or how to teach something | [Research and teaching decisions](research.md). Primary sources, both Streamlit repositories, and the design choices drawn from them. |
| Choosing what belongs on a particular day | [30-day syllabus](syllabus.md). Six sections, starting states, experiments, checks, and the gradual withdrawal of hints. |
| Writing a lesson | [Lesson authoring guide](lesson-guide.md). A seven-part lesson structure and worked lessons with predictions, hints, answer keys, and transfer tasks. |
| Helping a learner distinguish two plausible explanations | [Three contrasting cases](contrasting-cases.md). Similar-looking charts conceal different row orders, reference rules, or missing-data behaviour. |
| Checking what the learner can actually do | [Studio field guide](studio-reference.md). Tableau-to-ECharts translation, inspection surfaces, current capability boundaries, and common diagnoses. |
| Choosing a sample or verifying an expected result | [Dataset guide](datasets.md). Units, grain, known values, optional external sources, and proposed import choices. |
| Deciding whether someone has learned the skill | [Assessment and pilot](assessment.md). Six checkpoints, capstone briefs, a scoring guide, and a pilot observation sheet. |
| Picking up the project in a later session | [Delivery plan and decisions](delivery-plan.md). Current state, open decisions, next milestone, and what to update when the evidence changes. |

## Scope and teaching stance

The course concentrates on Cartesian charts that the builder can explain deeply. Bars, lines, scatter plots and heatmaps let learners explore stacking, area fills, size, colour, transforms, statistics, multiple axes, shared pointers, and responsive canvas layout. Pie charts, file export, and bringing your own data fall outside this edition. Familiar Tableau concepts are useful starting points. ECharts vocabulary and options are the language of the exercises and final walkthrough.

The full explorer stays available throughout. A lesson focuses attention through a question and a reproducible starting view. Learners can follow a curiosity, reverse an edit, and return to the question. The chart itself provides visual feedback. The option and data provide a readable way to check what happened.

**Current baseline.** The course is designed against the merged builder at `626bf89`, which uses native `st.echarts_chart`, DataFrames in `dataset.source`, twelve starting examples, and three bundled samples. The named examples already exist. The day sequence, new data integrations, and course navigation are proposals. A short recipe can already establish each core lesson’s starting state. [Builder at the reference revision](https://github.com/kieranadair/streamlit_echart_studio/tree/626bf892b02642785cd2af13c411529ef29e5f45)

To try the plan today, launch Studio, open **Bar chart** with **Monthly retail**, and follow day 1. The research, syllabus, and pilot cards are also readable directly on GitHub. [Run Studio locally](../../README.md#run-locally) · [Day 1 · Read axes and encodings](day-01.md) · [Day 8 · Trace a transform](day-08.md)

## How to use this reference over time

For a new day, read its syllabus entry, check the current builder and data guide, then use the lesson template. For a proposed feature, name the learner action or evidence it would enable and the day that would use it. Record a changed course decision in the delivery plan. Keep application implementation details and bug history with the application. The useful history here is **why a learner needs something and how we will know it helped**.
