# Data Source & Methodology

## Source

**NYC Open Data - Capital Projects Database (CPDB) - Projects** (public, no key required)
Dataset ID: `fi59-268w`
Endpoint: `https://data.cityofnewyork.us/resource/fi59-268w.csv`

This dataset is published by the NYC Office of Management and Budget (OMB)
and the Department of City Planning as part of the city's FY2026 Capital
Commitment Plan. It tracks every individually budgeted capital project
across NYC agencies: planned budget, planned start/completion dates,
amounts committed to contracts, and amounts actually spent.

## Sampling approach

- Filtered via the Socrata API to projects with a total planned commitment
  greater than $500,000 (`scripts/01_clean_data.py`), ordered by budget
  descending, capped at 600 rows returned by the API.
- Further filtered to rows where `typecategory = 'Fixed Asset'` - these are
  individually tracked capital construction projects (buildings, bridges,
  tunnels, water/sewer infrastructure), as opposed to "Lump Sum" program
  buckets or "ITT, Vehicles, and Equipment" purchases which aren't
  construction projects in the traditional sense.
- Result: 202 individual capital construction projects across 13 NYC
  agencies (DEP, DOT, DDC, SBS, DCAS, DPR, and others).
- No further filtering by agency, borough, or project status was applied -
  this is the full set of Fixed Asset projects above the budget threshold
  at the time of extraction.

## Fields kept

| Field | Description |
|---|---|
| `agency` | NYC agency code managing the project (DEP = Environmental Protection, DOT = Transportation, DDC = Design and Construction, etc.) |
| `description` | Project name |
| `mindate` | Planned project start date |
| `maxdate` | Planned project completion date |
| `planned_budget` | Total planned commitment for the project ($, FY26 Capital Plan) |
| `committed_to_date` | Amount actually committed to awarded contracts to date ($) |
| `spent_to_date` | Amount actually spent/disbursed to date ($) |

## Analysis "as-of" date

All schedule-status calculations in this project (e.g., "past planned
completion date") use **2026-07-21** as the reference date, since that is
when the extraction was run. Re-running the scripts later will change which
projects are flagged as overdue.

## Reproducing

```bash
python scripts/01_clean_data.py   # re-fetches live data, rebuilds data/construction.db
python scripts/02_analysis.py     # prints descriptive analysis
```

## Disclosure

This is a self-directed portfolio project built entirely on public NYC
Open Data for job-search purposes. It does not use, reference, or
represent any employer's proprietary data, models, or analysis.
