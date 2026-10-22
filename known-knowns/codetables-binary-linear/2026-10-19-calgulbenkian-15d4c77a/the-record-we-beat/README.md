# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=8&n=67&k=5 | 2026-10-19T04:35:44Z | 200 | fe307b0a8236ee9bf99090c81052f9423778bbcd056fd79328ca71fa3ff7ec38 | lower 54, upper 56 |
| BKLC neighbour [66,4] | http://www.codetables.de/BKLC/BKLC.php?q=8&n=66&k=4 | 2026-10-19T04:37:33Z | 200 | 2f574c7389c265dd667feb0cf86368fb7bc4d01c9a90a5300e73e591b5ce19cb | lower 56, upper 56 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) |
| BKLC neighbour [66,5] | http://www.codetables.de/BKLC/BKLC.php?q=8&n=66&k=5 | 2026-10-19T04:37:35Z | 200 | db499fdc2f23e7733b9d8ea4ab9f4bdda21f58157ca3666ad33b91e679a8ab1b | lower 53, upper 55 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) |
| BKLC neighbour [67,4] | http://www.codetables.de/BKLC/BKLC.php?q=8&n=67&k=4 | 2026-10-19T04:37:36Z | 200 | 5e7789fe755bf5da2c9bd87c45305f7d9a24bb2673c0e626a665bf8ff4483a68 | lower 56, upper 56 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) |
| BKLC neighbour [68,5] | http://www.codetables.de/BKLC/BKLC.php?q=8&n=68&k=5 | 2026-10-19T04:37:38Z | 200 | 0aae8d5984d0ecc7cbde1e1bfd7b9a2b122c5eba6a6cf458f50b6bbdcb102608 | lower 55, upper 56 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) |

Compared cell: [67,5] over GF(8). Live lower bound 54, upper bound 56. The certificate excludes d = 56.

cell_excerpt.txt copies the header line and Brouwer lines of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the four neighbouring cells with the offset of the propagation rule (the upper bound implied for the cell is the neighbour upper bound plus the offset).
