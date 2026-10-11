# Cleaning Log

Every step in `notebooks/01_cleaning.ipynb` that changes or removes rows, with row counts. The last cell of the notebook prints the table below; paste it here after each full run.

## Data snapshot

| Item | Value |
|---|---|
| Download date (UTC) | _from data/raw/download_manifest.json_ |
| `active_permits.csv` size | 68.3 MB |
| `cleared_permits_since_2017.csv` size | 149.6 MB |
| Active + Cleared rows combined (raw) | 646,015 |
| Rows after the 2017 filter | 437,705 |
| Rows after keeping the latest revision | 388,782 |
| Final clean rows | 388,263 |
| Distinct projects (`project_id`) | 206,516 (from the previous run; confirm on next run) |

## Steps

| # | Step | Rows before | Rows after | Rows removed | Why |
|---|---|---|---|---|---|
| 1 | Combine Active + Cleared | 646,015 | 646,015 | 0 | Both files share the same columns; a `source` column records where each row came from |
| 2 | Keep applications from 2017-01-01 onward | 646,015 | 437,705 | 208,310 | Project scope. The Cleared file includes permits applied for before 2017, so filtering on application date is required |
| 3 | Drop exact duplicate rows | 437,705 | 437,705 | 0 | Identical rows add no information |
| 4 | Keep latest revision per permit number | 437,705 | 388,782 | 48,923 | One row per permit. On a tie between files the Cleared copy is kept, because clearing happens after the active stage |
| 5 | Drop admin record types | 388,782 | 388,263 | 519 | DCs DeferredFees, Toronto Buildings Contacts, Toronto Building Standard Attachments, Building Historical data - Converted are records, not construction |

## Changes that do not remove rows

| Column | Change | Rows affected | Why |
|---|---|---|---|
| All text columns | Trimmed leading and trailing spaces | n/a | Stops values like "M5V " and "M5V" counting as different |
| `EST_CONST_COST` -> `est_cost` | Converted to number; placeholder text set to missing | 209,700 placeholder rows (219,380 missing in total, before the 2017 filter and dedupe) | Some rows hold "DO NOT UPDATE OR DELETE THIS INFO FIELD" instead of a cost. Not imputed, to avoid inventing values |
| `est_cost` overrides | Set to missing for 2 permits | 2 | A $1B sprinkler permit and a $500M retail interior teardown; descriptions do not fit the amounts |
| `cost_declared` | True when `est_cost` > 0 | 40,854 rows with cost exactly 0 treated as not declared; 128,548 rows had a declared cost before overrides | A real project rarely costs $0; value analyses use declared costs only |
| `POSTAL` -> `fsa` | Upper-cased, first 3 characters, must match M + digit + letter | 24,630 blank postal codes; no other invalid values | Territory unit for the analysis |
| `approval_days` | Negative values set to missing | 2 | Issue date before application date is a data error |
| `work_category` | Mapped from `WORK` values, falling back to `PERMIT_TYPE` | n/a | Categories: New construction, Addition, Renovation / alteration, Demolition, Building services, Other. Full mapping in notebook section 7 |
| `sector` | Keyword rules on `STRUCTURE_TYPE`, plus manual overrides (Duplex, Triplex, Converted House, Student Residence and others to Residential); "Other", "First Party", "Third Party" set to Unknown | n/a | Meaning of those two values is unclear, so they are not guessed |
| `is_related_permit`, `project_id` | Flag trade permits ("Building Permit Related" work) and group permits by number without the type code | n/a | About 175,000 trade permits would otherwise inflate activity counts. The project link is inferred from the permit number format |

## Decisions and open questions

- **Overlap between files (761 permit + revision pairs):** keep the Cleared copy. In sampled pairs the Cleared copy had a final status and a completed date while the Active copy still said "Inspection", and the Active copy's issued date matched the Cleared completed date, so the Active copy looked stale.
- **Active file has no completed dates:** `COMPLETED_DATE` was blank on all 202,298 Active rows.
- **Zero costs:** kept as published but excluded from value analysis via `cost_declared`.
- **Blank postal codes:** permits kept for city-wide counts, excluded from FSA maps.
- **Cancelled permits (33,324):** flagged with `is_cancelled`, not removed. _Decide in the Analyze phase whether to exclude them._
- **Trade permits (175,371):** flagged with `is_related_permit`. 388,263 permits group into about 206,500 projects.
- **Revised permits:** median approval time is 23 days for revised permits vs 29 for originals. The gap is modest, so revisions are kept as is and flagged with `is_revision`.
- **Blank postal codes:** concentrated in Conditional Permits (41% blank) and New Building permits (22% blank). FSA maps will under-count new buildings; state this as a limitation.
- **Non-numeric revision numbers (7 rows):** sorted so they are never chosen as the latest revision. This changed which row was kept for one admin-type permit, so step 5 removed 519 rows instead of 520.
- **Partial permits** are mapped to New construction, on the assumption that they are staged permits for large new buildings (foundation, shoring, framing).
- **Per-unit permits:** some townhouse developments file one New Houses permit per unit. In M2L, about 200 such permits from 2019 come from one development. Counts are left as published; this is noted where it affects results.
