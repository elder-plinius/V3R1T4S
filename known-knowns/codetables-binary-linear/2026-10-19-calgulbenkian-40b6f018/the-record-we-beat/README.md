# The record we beat (metadata and the one cell)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=4&n=157&k=10 | 2026-10-19T04:35:39Z | 200 | 16ce6e96ca31a9d96ed62987ebcb5d13214280eac6c5a1a432d65c997266fe21 | lower 101, upper 110 |

Compared cell: [157,10] over GF(4). Live lower bound 101, upper bound 110. This object: d = 102.

The excerpt of the page is in cell_excerpt.txt; live_bounds.json holds the two numbers read by verdict.py.
