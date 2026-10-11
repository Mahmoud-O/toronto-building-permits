"""
Build the data source for the Tableau Public dashboard.

Why a permit-level file instead of the summary tables?
  Tableau needs to compute medians (approval days) and growth rates at whatever
  level a chart shows: city, FSA, category, month. A median of pre-computed
  medians is not a real median, so we give Tableau one row per permit and let it
  aggregate correctly. The same filters as notebooks/02_analysis.ipynb are applied
  here, so the dashboard numbers match the notebook.

Run from the repo root on Windows (after 01_cleaning.ipynb has been run):
    py scripts\\export_tableau.py

Output: data/clean/tableau_permits.csv (not committed; Tableau Public stores a
copy of the data inside the published workbook).
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "clean"


def main() -> None:
    permits = pd.read_csv(
        CLEAN / "permits_clean.csv",
        parse_dates=["APPLICATION_DATE", "ISSUED_DATE", "app_year_month"],
        dtype={"PERMIT_NUM": str, "project_id": str, "fsa": str},
        low_memory=False,
    )
    for col in ["cost_declared", "is_cancelled", "is_revision", "is_related_permit"]:
        permits[col] = permits[col].astype(str).str.lower().eq("true")

    # Same analysis set as the notebook: real, distinct demand.
    demand = permits[~permits["is_cancelled"] & ~permits["is_related_permit"]].copy()

    # Same time rules as the notebook, worked out from the data.
    last_date = demand["APPLICATION_DATE"].max()
    last_full_month = (last_date.to_period("M") - 1).to_timestamp()
    last_full_year = last_full_month.year if last_full_month.month == 12 else last_full_month.year - 1
    recent = [last_full_year - 1, last_full_year]
    base = [last_full_year - 3, last_full_year - 2]

    out = pd.DataFrame({
        "permit_num": demand["PERMIT_NUM"],
        "project_id": demand["project_id"],
        "fsa": demand["fsa"],
        # Tableau guesses the country of a postcode from your computer's locale,
        # so "M4S" can be read as a US ZIP. A Country column fixes that.
        "country": "Canada",
        "application_date": demand["APPLICATION_DATE"].dt.date,
        "application_month": demand["app_year_month"].dt.date,
        "application_year": demand["app_year"],
        "sector": demand["sector"],
        "work_category": demand["work_category"],
        "permit_type": demand["PERMIT_TYPE"],
        "structure_type": demand["STRUCTURE_TYPE"],
        # Only declared costs (> 0); blank otherwise, so Tableau sums ignore them.
        "declared_value": demand["est_cost"].where(demand["cost_declared"]),
        # Approval days only for issued, non-revised permits (same rule as Q3).
        "approval_days": demand["approval_days"].where(~demand["is_revision"]),
        # Lets Tableau filter out the partial current month in trend charts.
        "is_full_month": demand["app_year_month"] <= last_full_month,
        # Growth windows for the FSA growth chart.
        "growth_window": demand["app_year"].map(
            lambda y: "recent" if y in recent else ("base" if y in base else "")
        ),
    })

    path = CLEAN / "tableau_permits.csv"
    out.to_csv(path, index=False)
    print(f"Saved {len(out):,} rows to {path}")
    print(f"Growth windows: base {base}, recent {recent}; last full month {last_full_month:%Y-%m}")


if __name__ == "__main__":
    main()
