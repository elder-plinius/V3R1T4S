# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| QECC qubit table, n 1..256 | https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 | 2026-10-19T04:34:26Z | 200 | 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6 | [[107,2]]: lower 23, upper 36; neighbours in neighbours.csv |

Compared cell: [[107,2]]. Live lower bound 23, upper bound 36. The certificate excludes d = 36, so the new upper bound is 35.

cell_excerpt.txt copies the extracted values; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the cells of the three propagation rules; pr_claims.csv lists the 56 values of merged and open pull requests for this target (from the pull-request list fetched 2026-10-19T04:30:31Z) that the triage treated as known bounds. verdict.py applies one step of each rule to the live values lowered by those pull-request values; the triage closure (all rules iterated over the whole table) is recorded in INDEX.csv.
