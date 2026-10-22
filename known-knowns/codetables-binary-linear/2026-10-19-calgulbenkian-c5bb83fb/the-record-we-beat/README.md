# The record we beat (metadata only)

One honest GET of the live cell, made by the orchestrator's triage agent. Only the cell excerpt is saved here, not the page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| codetables.de QECC cell | https://codetables.de/QECC.php?q=4&n=47&k=36 | 2026-10-19T06:10:56Z | 200 | 4c84e772c189b639a02184664831c9e0d4f5cfef5b49128d64d67dd9e1c651cc | [[47,36]], q=2: lower bound 3, upper bound 4; page says last modified: 2006-04-03 |

Excerpt saved as `cell_47_36_excerpt.txt`.

Compared cell: qubit stabilizer code [[47,36]]. Live lower bound 3, live upper bound 4. This object: d = 4, equal to the upper bound.

The triage agent also tested whether the lower bound 4 for this cell follows from other entries of the live full quantum table by the table's own propagation rules (its lowerclosure program on the full table fetched 2026-10-19T06:21:12Z, http 200, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6) and found that it does not.

Second fetch (the novelty skeptic, same URL): 2026-10-19T06:43:25Z, HTTP 200, page sha256 4c84e772c189b639a02184664831c9e0d4f5cfef5b49128d64d67dd9e1c651cc. Unchanged: lower bound 3, upper bound 4.
