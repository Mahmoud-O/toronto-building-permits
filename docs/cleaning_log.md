# Cleaning Log

Every step in `notebooks/01_cleaning.ipynb` that changes or removes rows, with row counts. The last cell of the notebook prints the table below; paste it here after each full run.

## Data snapshot

| Item | Value |
|---|---|
| Download date (UTC) | _from data/raw/download_manifest.json_ |
| Active Permits rows (raw) | _TBD_ |
| Cleared Permits since 2017 rows (raw) | _TBD_ |
| Final clean rows | _TBD_ |

## Steps

| # | Step | Rows before | Rows after | Rows removed | Why |
|---|---|---|---|---|---|
| 1 | Combine Active + Cleared | _TBD_ | _TBD_ | 0 | Both files share the same columns; a `source` column records where each row came from |
| 2 | Keep applications from 2017-01-01 onward | _TBD_ | _TBD_ | _TBD_ | Project scope. The Cleared file includes permits applied for before 2017, so filtering on application date is required |
| 3 | Drop exact duplicate rows | _TBD_ | _TBD_ | _TBD_ | Identical rows add no information |
| 4 | Keep latest revision per permit number | _TBD_ | _TBD_ | _TBD_ | One row per permit. On a tie between files the Cleared copy is kept, because clearing happens after the active stage |

## Changes that do not remove rows

| Column | Change | Rows affected | Why |
|---|---|---|---|
| All text columns | Trimmed leading and trailing spaces | n/a | Stops values like "M5V " and "M5V" counting as different |
| `EST_CONST_COST` -> `est_cost` | Converted to number; placeholder text set to missing | 209,700 placeholder rows (219,380 missing in total, before the 2017 filter and dedupe) | Some rows hold "DO NOT UPDATE OR DELETE THIS INFO FIELD" instead of a cost. Not imputed, to avoid inventing values |
| `cost_declared` | True when `est_cost` > 0 | 40,854 rows with cost exactly 0 treated as not declared | A real project rarely costs $0; value analyses use declared costs only |
| `POSTAL` -> `fsa` | Upper-cased, first 3 characters, must match M + digit + letter | 24,630 blank postal codes; no other invalid values | Territory unit for the analysis |
| `approval_days` | Negative values set to missing | 2 | Issue date before application date is a data error |
| `sector`, `work_category` | Grouped from `STRUCTURE_TYPE` and `WORK` | n/a | See mapping rules in the notebook, section 7 |

## Decisions and open questions

- **Overlap between files (761 permit + revision pairs):** keep the Cleared copy. In sampled pairs the Cleared copy had a final status and a completed date while the Active copy still said "Inspection", and the Active copy's issued date matched the Cleared completed date, so the Active copy looked stale.
- **Active file has no completed dates:** `COMPLETED_DATE` was blank on all 202,298 Active rows.
- **Zero costs:** kept as published but excluded from value analysis via `cost_declared`.
- **Blank postal codes:** permits kept for city-wide counts, excluded from FSA maps.
- **Cancelled permits:** flagged with `is_cancelled`, not removed. _Decide in the Analyze phase whether to exclude them._
- _Still open: category mapping for `sector` and `work_category`; whether revised permits distort approval days._
