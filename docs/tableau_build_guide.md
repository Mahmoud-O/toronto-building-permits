# Tableau Public Dashboard: Build Guide

The Share phase deliverable is one Tableau Public dashboard with four views. Each answers one guiding question, and each title states the finding.

| View | Question | Chart |
|---|---|---|
| 1. Where is the value? | Q1 | Filled map of FSAs, coloured by recent declared value |
| 2. Where is it growing? | Q1 | Bar chart of the 15 fastest-growing FSAs, with a city-wide reference line |
| 3. What and when? | Q2, Q4 | Monthly permits by type of work |
| 4. How fast? | Q3 | Median approval days by type of work |

## 0. Before you start

**M2L outlier (checked).** The 1,738-day median for new construction in M2L comes from one stacked back-to-back townhouse development: about 200 New Houses permits applied for in 2019, one per unit, issued roughly 4.8 years later. Mention it in a tooltip or footnote if M2L stands out in a view.

**Create the data file.** Tableau needs one row per permit so it can compute real medians and growth rates at any level:

```
py scripts\export_tableau.py
```

This writes `data/clean/tableau_permits.csv` using the same filters as `02_analysis.ipynb` (no cancelled permits, no trade permits tied to a building permit). It is not committed; Tableau Public keeps a copy inside the published workbook.

## 1. Connect the data

1. Open Tableau Public, choose **Text file**, and select `data/clean/tableau_permits.csv`.
2. On the data source page, check the types:
   - `application_date`, `application_month`: Date
   - `application_year`: change to **String** (Discrete) so it is not summed
   - `declared_value`, `approval_days`: Number (decimal)
   - `fsa`: String. Right-click it, choose **Geographic Role > ZIP Code/Postcode**.
3. Go to Sheet 1.

## 2. Calculated fields

Create these once (right-click in the Data pane, **Create Calculated Field**). Names matter, because later steps refer to them.

| Name | Formula | Why |
|---|---|---|
| `Permits` | `COUNT([permit_num])` | One row per permit |
| `Permits Recent` | `SUM(IF [growth_window] = "recent" THEN 1 ELSE 0 END)` | 2024-2025 permits |
| `Permits Base` | `SUM(IF [growth_window] = "base" THEN 1 ELSE 0 END)` | 2022-2023 permits |
| `Permit Growth` | `IF [Permits Base] >= 50 THEN [Permits Recent] / [Permits Base] - 1 END` | Same rule as the notebook: no rate for small areas |
| `City Growth` | `{ FIXED : SUM(IF [growth_window] = "recent" THEN 1 ELSE 0 END) } / { FIXED : SUM(IF [growth_window] = "base" THEN 1 ELSE 0 END) } - 1` | City-wide rate for the reference line. FIXED ignores the FSA breakdown |
| `Value Recent` | `SUM(IF [growth_window] = "recent" THEN [declared_value] END)` | Declared value in 2024-2025 |
| `Median Approval Days` | `MEDIAN([approval_days])` | Median, because approval times are heavily skewed |

Format `Permit Growth` and `City Growth` as **Percentage, 0 decimals**, and `Value Recent` as **Currency (Custom), Millions (M), 0 decimals**.

## 3. The four sheets

Colours: use one consistent palette (checked for colour-blind readers), always in this order, so a category keeps its colour everywhere:

| Category | Hex |
|---|---|
| Renovation / alteration | `#2a78d6` |
| New construction | `#eb6834` |
| Addition | `#1baf7a` |
| Demolition | `#eda100` |
| Single-colour bars | `#2a78d6` |
| Map (low to high) | `#cde2fb` to `#104281` |

### Sheet 1: Value map
1. Double-click `fsa`. Tableau draws a map. If it shows "unknown" locations, use **Map > Edit Locations** and set Country/Region to **Canada**.
2. Change the mark type to **Map** (filled).
3. Drag `Value Recent` to **Colour**. Edit colours: Sequential, custom from `#cde2fb` to `#104281`.
4. Drag `Permits Recent`, `Permit Growth` and `Value Recent` to **Tooltip**.
5. Title: **"10 of 98 FSAs hold 43% of recent declared construction value"**

*If the FSAs do not map:* Tableau's built-in Canadian postcode shapes should cover FSAs, but if they do not, download the Statistics Canada 2021 Census "Forward sortation areas" boundary file (cartographic, shapefile), add it as a second data source and relate `CFSAUID` to `fsa`.

### Sheet 2: Growth areas
1. Drag `fsa` to **Rows** and `Permit Growth` to **Columns**.
2. Right-click `fsa` > **Filter > Top** > by field: Top **15** by `Permit Growth`. Also filter out Null growth.
3. Sort descending by `Permit Growth`. Colour the bars `#2a78d6`.
4. Drag `City Growth` to **Detail**, then right-click the x-axis > **Add Reference Line** > Value: `City Growth` (Average), Label: Custom "City <Value>", dashed grey line.
5. Title: **"Growth is local: city-wide permits rose 1%, while M3C, M4A and M9A grew over 50%"**

### Sheet 3: Monthly trend
1. Drag `application_month` to **Columns**, set it to continuous **Month** (green pill).
2. Drag `Permits` to **Rows** and `work_category` to **Colour**.
3. Filters: `is_full_month` = True; `work_category` = Renovation / alteration, New construction, Addition, Demolition (Building services and Other are left out to keep the chart readable).
4. Apply the category colours above.
5. Title: **"Renovations lead every year; all work types fell in 2020 and peak each May to August"**

### Sheet 4: Approval time
1. Drag `work_category` to **Rows** and `Median Approval Days` to **Columns**.
2. Sort ascending. Colour bars `#2a78d6`. Turn on **Labels**.
3. Title: **"New construction waits 83 days at the median, about 3 times longer than renovations (27)"**

**Check every title against the chart.** The data and rules match the notebook, so the numbers should match. If one does not, the title changes, not the data.

## 4. The dashboard

1. **New Dashboard**. Size: **Fixed, 1200 x 900** (fits a laptop screen and exports cleanly).
2. Layout: title text box across the top; Sheet 1 and Sheet 2 side by side in the middle row; Sheet 3 and Sheet 4 side by side in the bottom row.
3. Dashboard title: **"Where Toronto construction demand is growing, 2017 to 2025"**
4. Add a `sector` filter from any sheet: click the sheet, open its menu, **Filters > sector**, then set **Apply to Worksheets > All Using This Data Source**.
5. Use the map as a filter: click the map sheet's menu and choose **Use as Filter**, so clicking an FSA updates the other views.
6. Footer text box: "Source: City of Toronto Open Data, Building Permits (Active and Cleared), Open Government Licence: Toronto. Excludes cancelled permits and trade permits tied to a building permit. Declared values are self-reported and not adjusted for inflation."

## 5. Publish and export

1. **File > Save to Tableau Public**. Name it "Toronto Building Permits: Where Construction Demand Is Growing".
2. Copy the public link.
3. Export images for the README: **Dashboard > Export Image** for the whole dashboard, saved as `outputs/figures/dashboard.png`. If that menu is greyed out, take a screenshot of the published dashboard at full size.
4. Send me the link and I will add it and the image to the README.

## What to commit after this phase

- `outputs/figures/dashboard.png`
- The README update with the link (I will make it)
- `scripts/export_tableau.py` and this guide are already committed
