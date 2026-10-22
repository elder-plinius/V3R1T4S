# The record we beat (metadata and the one cell)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=4&n=163&k=11 | 2026-10-19T04:35:36Z | 200 | 447e2d5ee68ef47d162dc8d39301b3739a324a85331159217b79dc95a0db2187 | lower 103, upper 113 |

Compared cell: [163,11] over GF(4). Live lower bound 103, upper bound 113. This object: d = 104.

The excerpt of the page is in cell_excerpt.txt; live_bounds.json holds the two numbers read by verdict.py.
