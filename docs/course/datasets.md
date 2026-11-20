# Dataset guide and checked values

Start with an inspectable chart and a real comparison. Use small familiar data where learners can check an answer by hand. Introduce an unfamiliar dataset when it helps distinguish a transferable skill from a memorised click sequence. The three Studio samples below are illustrative. The two external datasets are candidates for later integration. [Bundled sample definitions](https://github.com/kieranadair/streamlit_echart_studio/blob/626bf892b02642785cd2af13c411529ef29e5f45/echarts_studio/data.py)

## Assignments by section

| Days | Core data available now | Optional application to new data |
| --- | --- | --- |
| 1–5 · Read the contract | Monthly retail for comparison and typography, Regional channels for grain, Weather log for time and the checkpoint | Give a second retail month to check. Keeping the domain familiar frees attention for `dataset` and `encode`. |
| 6–10 · Order and orientation | Regional channels, with Weather log for two X fields | Rank the regions by Online after working with Stores. Ask for a region that changes rank. |
| 11–15 · Encodings | Regional channels in wide and long form, plus Weather log for gaps | **Palmer Penguins** for numeric position and bubble size. Keep the heatmap on Region–Channel, where the cell grain is already defined. |
| 16–20 · Annotations and calculations | Monthly retail for references and windows, Regional channels for the fit, Weather log for missing values | **AirPassengers** for a seasonal series and a twelve-observation mean. |
| 21–25 · Reader interaction | Regional channels for brushing, Monthly retail for linked panels and responsive layout | **Palmer Penguins** makes brushing worthwhile with hundreds of observations. Use species as a tooltip field to identify what was selected. |
| 26–30 · Independent transfer | Learner chooses one bundled sample and a new question | Offer either external dataset once its eligible lessons are available. A changed field, threshold, or reader constraint also provides transfer on a bundled sample. |

## Built-in samples

**Monthly retail.** Twelve rows, one per calendar month in the illustrative year. Month is an ordered sequence of category labels. Revenue and Target are monthly amounts in thousands of dollars. Sorting the abbreviations alphabetically would destroy the chronology. One monthly record can supply a Revenue bar and a Target line.

- March has Revenue 45 and Target 49. January, March, June, and September miss target across the full year. June’s pair is 56 and 60.
- The full-year Revenue sum is 781 against Target of 755, a $26,000 surplus. September has the largest miss at $5,000. The full-year mean Revenue is 65.0833. Keeping Revenue ≥ 50 retains April through December, nine rows totalling 646. Their mean is 71.7778 and their median is 68. A fixed policy threshold of 60 stays at 60.
- The first complete three-observation Revenue mean is 45 in March. The first complete four-observation mean is 48.25 in April. A peak marker identifies December at 98.

**Regional channels.** Six rows, one per region. Stores, Online, and Wholesale are additive sales amounts in thousands of dollars. Stores measures sales through that channel. When using the Heatmap starter, Studio reshapes the table to 18 rows with columns Region, Channel, and Sales. Channel is the category on the initial X axis, Region the Y category, and Sales the colour-driving dimension at zero-based index 2.

- Sorting Stores descending gives 81, 67, 61, 52, 43, 38. At ≥ 60 the rows are Eastern Seaboard, Central Valley, and Pacific Northwest.
- Pacific Northwest has Stores 61, Online 48, and Wholesale 20. The stack totals 129. The long-form Pacific Northwest × Online cell is 48 before and after transposition.
- Northern Coast has Online 39. The initial piecewise upper cutoffs are 39 and 60. Lowering the first cutoff to 38 moves that observation into the middle band. Western Plains’ Stores value of 38 stays in the low band.
- The Linear fit starter predicts Online from Stores. All six complete pairs give fitted endpoints near (38, 32.39) and (81, 57.53). At Stores ≥ 60 the remaining three pairs produce endpoints near (61, 47.69) and (81, 56.87). These Y coordinates are fitted values, distinct from observed sales.

**Weather log.** Sixty rows from 1 April to 30 May 2025. Date is a date field, Day is its sequential integer position, and High and Low are temperatures in °C. There is one row for each day, including the four with missing High. Converting to the heatmap sample produces one row per date and reading type, with date labels as categories.

- The first observation is day 1 with High 17.0 and Low 11.0. Choosing Day or Date for X preserves the observation.
- High is missing from 20 to 23 April inclusive. `connectNulls` can bridge the visual gap. A three-observation rolling High needs complete windows and resumes on 26 April at approximately 22.73 °C.
- Filtering Date to 1 May or later keeps 30 rows. This makes a useful check for a date parser or a date-versus-category lesson.

These values were checked against the baseline DataFrames and the builder’s calculated trend frames. If the generator changes, reproduce the pertinent calculations before revising the learner key. The filter and rolling implementations are short enough for an author to inspect. [Transforms and trend calculations](https://github.com/kieranadair/streamlit_echart_studio/blob/626bf892b02642785cd2af13c411529ef29e5f45/echarts_studio/datasets.py)

## External candidate 1 · Palmer Penguins

**Recommended first addition.** Use the simplified CSV from the authors’ `palmerpenguins` repository. It contains 344 measurement records, three species and three islands, with fieldwork spanning 2007–2009. The columns are `species`, `island`, `bill_length_mm`, `bill_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`, and `year`. Flipper length versus body mass provides 342 complete coordinate pairs. A third numeric field can drive point size. The species field gives a reason to configure tooltips and filtering. [Package and field descriptions](https://allisonhorst.github.io/palmerpenguins/) · [Pinned CSV](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/8957207b78d6ccd1b4654a9dd9c9041b657478ab/inst/extdata/penguins.csv)

**Preparation.** Keep a stable observation key for this snapshot, assigned before filtering or sorting. A source-row key is a teaching identifier. Keep the millimetre and gram units visible. Preserve missing readings, and count complete pairs only for the encoding or calculation being used. Eleven missing sex values are irrelevant to a flipper-length-versus-mass scatter plot. The canonical CSV includes year. The commonly used seaborn copy has a different column set and row ordering.

**Attribution.** Credit Horst, Hill, and Gorman for the package and Palmer Station LTER and Kristen Gorman for the observations, retaining the data citations and policy link supplied by the project. The project identifies the data as CC0. The lesson needs the tabular observations only. **Snapshot SHA-256** `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`. [Licence and citations at the pinned revision](https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/README.md#license)

**Compatible uses.** Scatter, bubble, filtering, numeric fitting, and brushing are good first targets. Summing body mass and flipper length in a stack has no interpretable unit. A species-by-island heatmap needs an explicitly chosen aggregate, such as count of records or median mass, and one row per resulting cell.

## External candidate 2 · Monthly international airline passengers

Use the small `flights.csv` from the seaborn sample repository as a convenient tabular version of the classic AirPassengers series. One row gives the monthly total of international passengers **in thousands**, January 1949 through December 1960. This is a time series of 144 monthly observations. It is easy to mistake the filename for a table of individual flights. [R dataset description and source](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/AirPassengers.html) · [Pinned CSV](https://raw.githubusercontent.com/mwaskom/seaborn-data/71e2436a092d714350de0fc409ca8a8714e7e78f/flights.csv)

**Preparation.** Parse `year` and the English `month` name to a first-of-month date, sort chronologically, and expose passengers as the measure. Retain the original fields for inspection. January 1949 is 112 thousand, July 1960 is 622 thousand, and the first twelve-month trailing mean is about 126.67 thousand in December 1949. A seasonal heatmap could use Year and Month as categories with one passenger total per cell. That would need a dedicated table shape. **Snapshot SHA-256** `237d834127d9c6355630d8f443a7a2377b5925923010009b59809ba0b67f4fac`.

**Provenance and availability.** R attributes the series to Box, Jenkins, and Reinsel. The seaborn repository describes its files as changeable examples and warns that some differ from canonical sources. The R description and seaborn README establish provenance but do not identify a dataset-specific redistribution licence for this CSV. Establish that basis before bundling it. The Weather log already supports the core window lesson. [Seaborn repository notes](https://github.com/mwaskom/seaborn-data/blob/71e2436a092d714350de0fc409ca8a8714e7e78f/README.md) · [R source notes](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/AirPassengers.html)

## Import recommendation for later implementation

Use `pandas.read_csv` on small, attributed snapshots packaged with the app. This uses an existing dependency, keeps the lesson reproducible, and removes a network download from Community Cloud startup. Record the source revision, checksum, units, preparation, and relevant terms beside each future snapshot. A Python plotting library adds little value solely as a data loader.

Offer each external dataset where the starter’s assumptions fit. For example, the current scatter starter expects two measures and the passenger series has one. Offer the passenger series for time-based lessons. A future integration should check row count, unique grain, null policy, units, and one known result in each supported starter. All thirty core days already have a bundled-data route.
