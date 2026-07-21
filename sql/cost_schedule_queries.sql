-- cost_schedule_queries.sql
-- SQL analysis queries for the NYC capital construction projects sample,
-- run against the SQLite database at data/construction.db
-- (build it first with: python scripts/01_clean_data.py)
--
-- Table: capital_projects
-- Columns: agency, description, mindate, maxdate, planned_budget,
--          committed_to_date, spent_to_date
--
-- "As-of" date used throughout: 2026-07-21
--
-- Key concepts:
--   cost variance    = (committed_to_date - planned_budget) / planned_budget
--   schedule status  = whether maxdate (planned completion) has passed,
--                       cross-referenced with how much of the budget has
--                       actually been spent

-- 1. Portfolio overview: how many projects have started, and how much of
--    their combined budget has been committed to contracts so far?
SELECT
    COUNT(*) AS started_projects,
    SUM(planned_budget) AS total_planned_budget,
    SUM(committed_to_date) AS total_committed,
    ROUND(100.0 * SUM(committed_to_date) / SUM(planned_budget), 1) AS pct_committed
FROM capital_projects
WHERE mindate <= '2026-07-21';

-- 2. Cost variance ranking: projects where committed contract value already
--    exceeds (or comes closest to exceeding) the total planned commitment.
SELECT
    description, agency, planned_budget, committed_to_date,
    ROUND(100.0 * (committed_to_date - planned_budget) / planned_budget, 1) AS cost_variance_pct
FROM capital_projects
WHERE mindate <= '2026-07-21' AND planned_budget > 0
ORDER BY cost_variance_pct DESC
LIMIT 10;

-- 3. Projects already over their total planned commitment (true cost overruns).
SELECT
    description, agency, planned_budget, committed_to_date,
    ROUND(100.0 * (committed_to_date - planned_budget) / planned_budget, 1) AS cost_variance_pct
FROM capital_projects
WHERE mindate <= '2026-07-21' AND committed_to_date > planned_budget
ORDER BY cost_variance_pct DESC;

-- 4. Schedule risk: projects past their planned completion date, ranked by
--    how little of the budget has actually been spent (a proxy for delay).
SELECT
    description, agency, maxdate, planned_budget, spent_to_date,
    ROUND(100.0 * spent_to_date / planned_budget, 1) AS pct_spent
FROM capital_projects
WHERE maxdate < '2026-07-21' AND mindate <= '2026-07-21'
ORDER BY pct_spent ASC;

-- 5. Agency-level portfolio summary: total budget, number of projects, and
--    contract commitment pace by managing agency.
SELECT
    agency,
    COUNT(*) AS n_projects,
    SUM(planned_budget) AS total_planned_budget,
    ROUND(100.0 * SUM(committed_to_date) / SUM(planned_budget), 1) AS pct_committed
FROM capital_projects
WHERE mindate <= '2026-07-21'
GROUP BY agency
ORDER BY total_planned_budget DESC;

-- 6. Largest capital projects overall (started or not), regardless of
--    commitment status - a view of the biggest bets in the portfolio.
SELECT
    description, agency, mindate, maxdate, planned_budget
FROM capital_projects
ORDER BY planned_budget DESC
LIMIT 10;

-- 7. Planned project duration (in days) by agency - highlights which
--    agencies run the longest-duration capital delivery programs.
SELECT
    agency,
    COUNT(*) AS n_projects,
    ROUND(AVG(JULIANDAY(maxdate) - JULIANDAY(mindate)), 0) AS avg_planned_duration_days
FROM capital_projects
WHERE mindate IS NOT NULL AND maxdate IS NOT NULL
GROUP BY agency
HAVING COUNT(*) >= 3
ORDER BY avg_planned_duration_days DESC;
