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
| `EST_CONST_COST` -> `est_cost` | Converted to number; placeholder text set to missing | _TBD_ | Some rows hold "DO NOT UPDATE OR DELETE THIS INFO FIELD" instead of a cost. Not imputed, to avoid inventing values |
| `POSTAL` -> `fsa` | Upper-cased, first 3 characters, must match M + digit + letter | _TBD invalid_ | Territory unit for the analysis |
| `approval_days` | Negative values set to missing | _TBD_ | Issue date before application date is a data error |
| `sector`, `work_category` | Grouped from `STRUCTURE_TYPE` and `WORK` | n/a | See mapping rules in the notebook, section 7 |

## Decisions and open questions

- _Record any decision made while reviewing the CHECK cells here (for example, how the "Other" work category was resolved)._
