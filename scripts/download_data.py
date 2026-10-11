"""
Download the City of Toronto building permit datasets into data/raw/.

Source: City of Toronto Open Data portal (CKAN), Open Government Licence: Toronto.
  - Building Permits: Active Permits   (package id: building-permits-active-permits)
  - Building Permits: Cleared Permits  (package id: building-permits-cleared-permits)

Why ask the CKAN API instead of hard-coding file URLs?
  The portal sometimes renames or replaces resources (the Cleared dataset used to
  be one file per year and is now a single "since 2017" file). Looking the
  resources up at run time means the script keeps working when that happens, and
  it records exactly which resource ids were downloaded, which makes the analysis
  reproducible.

Run from the repo root on Windows:
    py scripts\\download_data.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# Repo root is one level above this scripts/ folder, so the script works
# no matter which folder you run it from.
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# package id on the portal -> local file name we save it as.
# For Cleared we want the "since 2017" resource, not the older "2000 to 2016"
# archive, because the project scope is applications from 2017 onward.
DATASETS = {
    "building-permits-active-permits": {
        "out_file": "active_permits.csv",
        "name_must_contain": None,
    },
    "building-permits-cleared-permits": {
        "out_file": "cleared_permits_since_2017.csv",
        "name_must_contain": "since 2017",
    },
}


def get_package(package_id: str) -> dict:
    """Return the CKAN metadata (including the list of resources) for one dataset."""
    resp = requests.get(
        f"{BASE_URL}/api/3/action/package_show",
        params={"id": package_id},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["result"]


def pick_csv_resource(package: dict, name_must_contain: str | None) -> dict:
    """
    Choose the resource to download.

    We prefer the "datastore" CSV (datastore_active = True). That is the table the
    portal itself serves through its API, so it is the canonical copy. If an
    optional name filter is given, the resource name must contain it.
    """
    candidates = [
        r for r in package["resources"]
        if r.get("format", "").upper() == "CSV"
        and r.get("datastore_active")
        and (name_must_contain is None
             or name_must_contain.lower() in r.get("name", "").lower())
    ]
    if not candidates:
        names = [r.get("name") for r in package["resources"]]
        raise RuntimeError(
            f"No matching CSV resource in {package['name']}. "
            f"Resources found: {names}. The portal may have changed; "
            "update DATASETS in this script."
        )
    return candidates[0]


def download(url: str, out_path: Path) -> int:
    """Stream the file to disk in chunks (the files are hundreds of MB, so we
    avoid loading them into memory). Returns the number of bytes written."""
    written = 0
    with requests.get(url, stream=True, timeout=300) as resp:
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                written += len(chunk)
    return written


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {"downloaded_at_utc": datetime.now(timezone.utc).isoformat(), "files": []}

    for package_id, cfg in DATASETS.items():
        package = get_package(package_id)
        resource = pick_csv_resource(package, cfg["name_must_contain"])

        # The datastore "dump" endpoint returns the whole table as CSV.
        url = f"{BASE_URL}/datastore/dump/{resource['id']}"
        out_path = RAW_DIR / cfg["out_file"]

        print(f"Downloading '{resource['name']}' from {package_id} ...")
        n_bytes = download(url, out_path)
        print(f"  saved {out_path.name} ({n_bytes / 1e6:,.1f} MB)")

        manifest["files"].append({
            "package_id": package_id,
            "resource_id": resource["id"],
            "resource_name": resource["name"],
            "url": url,
            "local_file": out_path.name,
            "bytes": n_bytes,
        })

    # A small record of what was downloaded and when. This goes in the cleaning
    # log so anyone can see which snapshot of the daily-refreshed data was used.
    manifest_path = RAW_DIR / "download_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {manifest_path.name}")


if __name__ == "__main__":
    main()
