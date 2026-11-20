# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=7&n=55&k=10 | 2026-10-19T04:35:46Z | 200 | b805d923e10bc518778186de0c10abd652734aafc3347baf1422eb19883fbc1b | lower 34, upper 40 |
| BKLC neighbour [54,9] | http://www.codetables.de/BKLC/BKLC.php?q=7&n=54&k=9 | 2026-10-19T04:37:25Z | 200 | 051fb89c6fe0c6cc2e13becc5d84e8e95684062e9e9f9578fb72ac7419e851dd | lower 35, upper 40 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) |
| BKLC neighbour [54,10] | http://www.codetables.de/BKLC/BKLC.php?q=7&n=54&k=10 | 2026-10-19T04:37:27Z | 200 | 54a8940417c9fc4d61ea407e1768c3831fdc80fbf9c8bb3edd621c98a76934ae | lower 33, upper 39 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) |
| BKLC neighbour [55,9] | http://www.codetables.de/BKLC/BKLC.php?q=7&n=55&k=9 | 2026-10-19T04:37:29Z | 200 | 2c2932b02fe4f488bff08a660daee2c3102257f0733ba01d99904c556b3e927b | lower 36, upper 41 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) |
| BKLC neighbour [56,10] | http://www.codetables.de/BKLC/BKLC.php?q=7&n=56&k=10 | 2026-10-19T04:37:32Z | 200 | 91117f9f9284e0fb6e3b9a92f9c9dbb95004ea1092e58f5e1df59dfb577e6049 | lower 35, upper 41 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) |

Compared cell: [55,10] over GF(7). Live lower bound 34, upper bound 40. The certificate excludes d = 40.

cell_excerpt.txt copies the header line and Brouwer lines of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the four neighbouring cells with the offset of the propagation rule (the upper bound implied for the cell is the neighbour upper bound plus the offset).
