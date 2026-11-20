# The record we beat (metadata and the cell)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| QECC cell page | https://codetables.de/QECC.php?q=4&n=23&k=9 | 2026-10-19T04:35:06Z | 200 | 5ba0fab508fc0ef72a89d75af4cedf5279e60758efa55e99ac1414f15875a6a7 | lower 4, upper 6 |
| QECC full table (neighbour cells) | https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 | 2026-10-19T04:34:26Z | 200 | 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6 | neighbour cells in neighbours.csv |

Compared cell: [[23,9]]. Live lower bound 4, upper bound 6. This object: d = 5.

cell_excerpt.txt is the header line of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the neighbouring cells (live lower, upper) with the offset applied by each propagation rule.
