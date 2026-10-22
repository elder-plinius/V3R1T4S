# The record we compare against (metadata and saved rows)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent. No page is copied here.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| orrick_page3.shtml | https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/page3.shtml | 2026-10-19T04:32:34Z | 200 | bc7cbefba3246001d08c04c6e5f8542d599074b28ded9fb6baca289c64f742d5 | row n = 105: order 105: value 3.847437473E74, flag '??' (not proved), ratio to the bound .70 |
| caltech_maxdet_records.csv | https://raw.githubusercontent.com/Math-AI-Caltech/hadamard-maxdet/main/maxdet_records.csv | 2026-10-19T04:32:34Z | 200 | 884d99a5b8ffd1a699a1f90b2f46b429323e7fc6fe3a037706dff5d8117ff2c9 | no row for order 105 (rows exist for n = 51, 103, 107, 111, 115, 119 and others; saved header and row list in caltech_orders.txt) |

Compared cell: order 105, normalised determinant. Orrick value: 3.847437473E74 (not proved). 
