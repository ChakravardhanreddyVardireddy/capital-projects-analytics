"""
01_clean_data.py

Fetches capital construction project data directly from the live NYC Open
Data (Socrata) API, filters to individual "Fixed Asset" construction
projects, computes cost/schedule variance flags, and loads the result
into a local SQLite database for SQL analysis.

Data source
-----------
NYC Open Data - Capital Projects Database (CPDB) - Projects
Dataset: fi59-268w
API endpoint used:
  https://data.cityofnewyork.us/resource/fi59-268w.csv
Filtered to projects with a total planned commitment greater than
$500,000, which are individually tracked capital construction projects
(as opposed to citywide equipment/vehicle purchases). See
data/DATA_SOURCE.md for full methodology notes.

Key fields kept:
  agency              - NYC agency managing the project (DEP, DOT, DDC, etc.)
  description         - project name/description
  mindate / maxdate    - planned start / planned completion date
  planned_budget      - total planned commitment ($ FY26 Capital Plan)
  committed_to_date   - amount actually committed to contracts to date
  spent_to_date       - amount actually spent/disbursed to date

Usage
-----
python scripts/01_clean_data.py
"""

import sqlite3
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
API_BASE = "https://data.cityofnewyork.us/resource/fi59-268w.csv"

SELECT_FIELDS = (
    "magencyacro,description,typecategory,mindate,maxdate,"
    "totalplannedcommit,commit_total,spent_total"
)
WHERE_CLAUSE = "totalplannedcommit>500000"
ORDER_CLAUSE = "totalplannedcommit DESC"
LIMIT = 600


def fetch_raw() -> pd.DataFrame:
    """Pull the capital projects extract from the live NYC Open Data API."""
    query = (
        f"$select={quote(SELECT_FIELDS)}"
        f"&$where={quote(WHERE_CLAUSE)}"
        f"&$order={quote(ORDER_CLAUSE)}"
        f"&$limit={LIMIT}"
    )
    url = f"{API_BASE}?{query}"
    with urlopen(url, timeout=30) as resp:
        raw_text = resp.read().decode("utf-8")
    raw_path = DATA_DIR / "projects_raw.csv"
    raw_path.write_text(raw_text, encoding="utf-8")
    return pd.read_csv(raw_path, engine="python", on_bad_lines="skip")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Keep individually-tracked Fixed Asset construction projects only."""
    df = df[df["typecategory"] == "Fixed Asset"].copy()
    df["mindate"] = pd.to_datetime(df["mindate"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["maxdate"] = pd.to_datetime(df["maxdate"], errors="coerce").dt.strftime("%Y-%m-%d")
    df = df.rename(columns={
        "magencyacro": "agency",
        "totalplannedcommit": "planned_budget",
        "commit_total": "committed_to_date",
        "spent_total": "spent_to_date",
    })
    return df[["agency", "description", "mindate", "maxdate",
               "planned_budget", "committed_to_date", "spent_to_date"]]


def main():
    raw = fetch_raw()
    print(f"Fetched {len(raw)} raw project rows")

    clean_df = clean(raw)
    print(f"Kept {len(clean_df)} Fixed Asset construction projects")

    clean_path = DATA_DIR / "construction_sample.csv"
    clean_df.to_csv(clean_path, index=False)
    print(f"Wrote clean data to {clean_path}")

    db_path = DATA_DIR / "construction.db"
    conn = sqlite3.connect(db_path)
    clean_df.to_sql("capital_projects", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded data into SQLite database at {db_path}")


if __name__ == "__main__":
    main()
