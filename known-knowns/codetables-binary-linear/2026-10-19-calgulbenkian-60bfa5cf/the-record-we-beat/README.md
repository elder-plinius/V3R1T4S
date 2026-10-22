# The record we beat (metadata and the one cell)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=4&n=160&k=11 | 2026-10-19T04:35:33Z | 200 | 66940d1d63a32c585d0466f9bfc9bdbccacc4ec0b8448439efd301b3fb0ed955 | lower 101, upper 111 |

Compared cell: [160,11] over GF(4). Live lower bound 101, upper bound 111. This object: d = 102.

The excerpt of the page is in cell_excerpt.txt; live_bounds.json holds the two numbers read by verdict.py.
