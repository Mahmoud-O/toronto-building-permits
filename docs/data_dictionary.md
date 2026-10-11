# Data Dictionary

## Raw columns

Column names and published types below come from the City of Toronto Open Data API (datastore schema for both resources, checked 2026-10-11). Active and Cleared share the same 32 columns. Descriptions marked **(confirm)** are my reading of the column name and a few sample rows, not official definitions; confirm them against the real files and the dataset page's documentation.

| Column | Published type | Description |
|---|---|---|
| `_id` | int | Row number added by the portal. Dropped during cleaning |
| `PERMIT_NUM` | text | Permit number, e.g. "24 110570 HVA": two-digit year, application number, and a permit sub-type code. Related permits for one project share the middle number **(confirm)** |
| `REVISION_NUM` | text | Revision of the permit, e.g. "00", "01" |
| `PERMIT_TYPE` | text | Type of permit, e.g. "Partial Permit" |
| `STRUCTURE_TYPE` | text | Type of building, e.g. "Apartment Building", "Mixed Use/Res w Non Res" |
| `WORK` | text | Type of work, e.g. "Partial Permit - Foundation" |
| `STREET_NUM`, `STREET_NAME`, `STREET_TYPE`, `STREET_DIRECTION` | text | Address parts |
| `POSTAL` | text | Postal code. In the sample rows seen, only the first three characters (FSA) were present **(confirm)** |
| `GEO_ID` | text | City geographic id for the address **(confirm)** |
| `WARD_GRID` | text | Ward and grid reference, e.g. "S0423" **(confirm)** |
| `APPLICATION_DATE` | date | Date the permit application was made |
| `ISSUED_DATE` | date | Date the permit was issued (blank if not yet issued) |
| `COMPLETED_DATE` | date | Date the permit was completed or closed **(confirm)** |
| `STATUS` | text | Current status, e.g. "Permit Issued", "Inspection", "Closed", "Superseded" |
| `DESCRIPTION` | text | Free-text description of the work |
| `CURRENT_USE`, `PROPOSED_USE` | text | Use of the property before and after the work |
| `DWELLING_UNITS_CREATED`, `DWELLING_UNITS_LOST` | text | Housing units added or removed. Units lost is rarely filled in |
| `EST_CONST_COST` | text | Declared estimated construction cost (self-reported). Contains placeholder text on some trade permits |
| `ASSEMBLY`, `INSTITUTIONAL`, `RESIDENTIAL`, `BUSINESS_AND_PERSONAL_SERVICES`, `MERCANTILE`, `INDUSTRIAL`, `INTERIOR_ALTERATIONS`, `DEMOLITION` | float | Floor area by occupancy or work category **(confirm units, likely square metres)** |
| `BUILDER_NAME` | text | Builder, often blank. Not used in the analysis |

## Derived columns (created in 01_cleaning.ipynb)

| Column | Type | How it is built |
|---|---|---|
| `fsa` | text | First 3 characters of `POSTAL`, upper case; missing if it is not M + digit + letter |
| `app_year` | int | Year of `APPLICATION_DATE` |
| `app_month` | int | Month number (1 to 12) of `APPLICATION_DATE` |
| `app_year_month` | date | First day of the application month, for monthly trends |
| `approval_days` | float | `ISSUED_DATE` minus `APPLICATION_DATE` in days; missing if not issued or negative |
| `est_cost` | float | `EST_CONST_COST` as a number; missing where the source is not numeric |
| `sector` | text | Residential, Non-residential, Mixed use or Unknown, from `STRUCTURE_TYPE` keywords |
| `work_category` | text | New construction, Addition, Renovation / alteration, Demolition or Other, from `WORK` keywords |
| `source` | text | "active" or "cleared": which file the kept row came from |
