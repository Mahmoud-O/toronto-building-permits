# Toronto Building Permits: Where Is Construction Demand Growing?

Capstone case study for the Google Data Analytics Professional Certificate, using real City of Toronto open data instead of the provided Cyclistic or Bellabeat datasets.

## Scenario

A Toronto building supply company wants to know where construction demand is growing so it can focus its sales reps and inventory.

**Business task:** identify where in Toronto construction activity is growing, what kind of work it is, and how quickly permits move, so the sales team can focus territory and product mix on the strongest demand.

**Stakeholders:** sales leadership, executive team, operations and inventory, analytics team.

## Guiding questions

1. Where is permit activity (count and declared construction value) concentrated and growing?
2. How is activity split between residential and non-residential, and new construction vs additions vs renovations?
3. How long do permits take from application to issuance, and does that vary by type or area?
4. How have volumes and values changed over time, and what seasonal patterns exist?

**Territory unit:** Forward Sortation Area (FSA), the first three characters of a postal code.

## Data

City of Toronto Open Data, released under the [Open Government Licence: Toronto](https://open.toronto.ca/open-data-license/):

- [Building Permits: Active Permits](https://open.toronto.ca/dataset/building-permits-active-permits/) (refreshed daily)
- [Building Permits: Cleared Permits](https://open.toronto.ca/dataset/building-permits-cleared-permits/) (the "Cleared Building Permits since 2017" file)

Scope: permits applied for from 1 January 2017 onward. The two datasets are combined, overlaps removed, and the latest revision kept per permit number.

**Known limitations:** permits signal intent, not completed construction; declared cost is self-reported and missing for many trade permits; dwelling units lost is rarely filled in; large projects carry several related permits that can inflate counts.

## Dashboard

_Tableau Public link and screenshot to be added in the Share phase._ Build steps: [docs/tableau_build_guide.md](docs/tableau_build_guide.md).

## Repository layout

```
toronto-building-permits/
  README.md
  requirements.txt
  data/raw/            raw downloads (not committed; run scripts/download_data.py)
  data/clean/          cleaned table (not committed; rebuilt by 01_cleaning.ipynb)
  notebooks/
    01_cleaning.ipynb  Process phase
    02_analysis.ipynb  Analyze phase
  outputs/figures/
  outputs/summary_tables/
  docs/
    cleaning_log.md    every cleaning step and the rows it affected
    data_dictionary.md raw and derived columns
    tableau_build_guide.md  step-by-step dashboard build
  scripts/
    download_data.py   fetches both datasets from the City's open data API
    export_tableau.py  builds the permit-level data source for the dashboard
```

## How to reproduce (Windows)

```
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py scripts\download_data.py
jupyter notebook notebooks\01_cleaning.ipynb
```

## Project status

| Phase | Status | Output |
|---|---|---|
| Ask, Prepare | Done | Case study document |
| Process | Done | `scripts/download_data.py`, `notebooks/01_cleaning.ipynb`, `docs/` |
| Analyze | Done | `notebooks/02_analysis.ipynb`, `outputs/summary_tables/` |
| Share | In progress | Tableau Public dashboard |
| Act | Not started | Write-up, slide deck, portfolio page |
