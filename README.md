# NYC Capital Construction Cost & Schedule Variance Analysis

**Self-directed portfolio project** analyzing cost and schedule variance
across NYC's capital construction program using real, public city budget
data. Built to demonstrate SQL and Python analysis skills for business/data
analyst roles in AEC (architecture, engineering, construction) and public
infrastructure delivery, informed by a civil engineering background. Not
affiliated with or representative of any employer's work.

[View the live dashboard](dashboard/index.html)

## Business problem

Capital program managers and construction owners need to know, across a
large portfolio of projects, which ones are running over budget and which
are falling behind schedule - before those problems compound. This project
asks three questions a construction/capital-program analyst would ask of a
city's capital plan:

1. How much of the capital portfolio's planned budget has actually been committed to contracts, and where are commitments already exceeding the plan?
2. Which specific projects are past their planned completion date without having spent their budget - a sign of stalled delivery?
3. Which agencies are managing the largest capital programs, and how does their contracting pace compare?

## Dataset

**Source:** [NYC Open Data - Capital Projects Database (CPDB), dataset fi59-268w](https://data.cityofnewyork.us/City-Government/Capital-Projects-Database-CPDB-Projects/fi59-268w)
(public, no authentication required)

- 202 individually tracked "Fixed Asset" capital construction projects
  (buildings, bridges, tunnels, water/sewer infrastructure) with a planned
  budget over $500,000, spanning 13 NYC agencies.
- Pulled live from the Socrata API, filtered to construction projects only
  (excluding lump-sum program buckets and equipment/vehicle purchases).
  See [`data/DATA_SOURCE.md`](data/DATA_SOURCE.md) for full sourcing and
  filtering methodology.
- Key fields: managing agency, planned start/completion dates, total
  planned budget, amount committed to contracts, amount actually spent.

## Methodology

1. **Extract** - `scripts/01_clean_data.py` pulls live capital project data from the NYC Open Data Socrata API.
2. **Clean** - filter to Fixed Asset (construction) projects; parse planned start/completion dates; rename fields for clarity.
3. **Analyze** - `scripts/02_analysis.py` (pandas) and `sql/cost_schedule_queries.sql` (7 annotated SQL queries, verified against a local SQLite database) compute cost variance, schedule risk, and agency-level portfolio summaries, using 2026-07-21 as the analysis "as-of" date.
4. **Visualize** - `dashboard/index.html`, a self-contained interactive Plotly dashboard (no server required - open directly in a browser).

## Key findings

- **Of the 157 projects already underway, only 18.7% of their combined $49.2B planned budget has been committed to contracts** - reflecting the long, front-loaded planning phase typical of major municipal capital works.
- **Two projects have already committed more than their entire planned budget**: the DEP's "Modification of Chambers at Hillview" water infrastructure project has committed $837M against a $353M plan - a 137% cost variance - and the "Reconstruction of Primary Tanks at North River WPCP" is 3% over its plan.
- **Four projects are past their planned completion date, and three show clear signs of delay**: DEP's Community Wastewater Planning Assistance (0% spent), a DCAS Lab Relocation (0% spent), and a DEP tide-gate replacement (3.9% spent) have all passed their target completion dates with minimal budget execution - while DOT's Brooklyn Bridge Hazard Mitigation project is a schedule success, landing at 100% spent right at its planned completion date.
- **DDC (Design and Construction) and DEP (Environmental Protection) together account for $31.3B of the $49.2B in started-project budget** - roughly two-thirds of the active portfolio - making them the two agencies where portfolio-level risk monitoring matters most.
- **DOT has committed only 3.1% of its $9.9B in started-project budget**, the lowest contracting pace of any major agency in the sample, worth flagging for a closer look at procurement bottlenecks.
- **The median planned project duration is 9 years**, underscoring how long major civil infrastructure delivery cycles run and why early cost/schedule signals matter disproportionately.

## Recommendations

1. **Escalate the two projects already over their planned commitment** (Hillview Chambers Modification and North River WPCP Primary Tanks) for scope and change-order review before further contracts are awarded.
2. **Investigate the three delayed, past-due, low-spend projects** (Community Wastewater Planning, DEP Lab Relocation, tide-gate replacement) to determine whether they need re-baselined schedules or are effectively stalled.
3. **Prioritize portfolio oversight at DDC and DEP**, which together represent roughly two-thirds of active capital spending in this sample - even small percentage-point improvements in contracting pace there move the most dollars.
4. **Use spend-to-date-versus-time-elapsed as a standing early-warning metric** rather than waiting for a project to pass its planned completion date, since by then (as seen here) the delay is already established.

## Repo structure

```
capital-projects-analytics/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── DATA_SOURCE.md
│   └── construction_sample.csv     # 202-project sample (static, committed)
├── scripts/
│   ├── 01_clean_data.py            # fetches live from NYC Open Data API
│   └── 02_analysis.py              # pandas descriptive analysis
├── sql/
│   └── cost_schedule_queries.sql   # 7 annotated SQL queries
└── dashboard/
    ├── index.html                  # interactive Plotly dashboard
    └── chart_data.json
```

## Running this project

```bash
pip install -r requirements.txt
python scripts/01_clean_data.py    # optional: re-fetches live data, rebuilds data/construction.db
python scripts/02_analysis.py      # prints the analysis in the terminal
```

Open `dashboard/index.html` directly in a browser - no server needed.

To run the SQL queries, build the database first (`python scripts/01_clean_data.py`), then run `sql/cost_schedule_queries.sql` against `data/construction.db` with any SQLite client.

## Tools

Python (pandas), SQL (SQLite), Plotly (interactive dashboard). Data sourced
live from the NYC Open Data public API (Socrata).

---
*This is a self-directed portfolio project built on public NYC Open Data
for job-search purposes. It does not represent any employer's proprietary
work.*
