# The record we beat (metadata only)

One honest GET of the live cell, made by the orchestrator's triage agent. Only the cell excerpt is saved here, not the page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| codetables.de QECC cell | https://codetables.de/QECC.php?q=4&n=49&k=38 | 2026-10-19T06:10:56Z | 200 | ff9ff1bf84b2e6675377943e0e48d63951ae2b494371d62617a0fa57254f7eec | [[49,38]], q=2: lower bound 3, upper bound 4; page says last modified: 2006-04-03 |

Excerpt saved as `cell_49_38_excerpt.txt`.

Compared cell: qubit stabilizer code [[49,38]]. Live lower bound 3, live upper bound 4. This object: d = 4, equal to the upper bound.

The triage agent also tested whether the lower bound 4 for this cell follows from other entries of the live full quantum table by the table's own propagation rules (its lowerclosure program on the full table fetched 2026-10-19T06:21:12Z, http 200, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6) and found that it does not.

Second fetch (the novelty skeptic, same URL): 2026-10-19T06:43:25Z, HTTP 200, page sha256 ff9ff1bf84b2e6675377943e0e48d63951ae2b494371d62617a0fa57254f7eec. Unchanged: lower bound 3, upper bound 4.
