# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=5&n=66&k=11 | 2026-10-19T04:35:47Z | 200 | 1e895e2039327b4e5f7f937354d6b46af141ba8499f01bdb196837148077ca97 | lower 38, upper 45 |
| BKLC neighbour [65,10] | http://www.codetables.de/BKLC/BKLC.php?q=5&n=65&k=10 | 2026-10-19T04:37:19Z | 200 | b1bd181cdf5e0253a369cfad33e99219a998360332356f7d5685a2422819c6ba | lower 39, upper 45 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) |
| BKLC neighbour [65,11] | http://www.codetables.de/BKLC/BKLC.php?q=5&n=65&k=11 | 2026-10-19T04:37:21Z | 200 | 36e1e2aa80b8460a3eea2ddc4732f443c01cab50cfbebc42f8bbc4e3b97a9342 | lower 37, upper 44 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) |
| BKLC neighbour [66,10] | http://www.codetables.de/BKLC/BKLC.php?q=5&n=66&k=10 | 2026-10-19T04:37:22Z | 200 | bb2df87369b4c3dc92eb4cb2d349c15a063bc357cd9d5a5f7eeb3fe29338feb9 | lower 40, upper 45 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) |
| BKLC neighbour [67,11] | http://www.codetables.de/BKLC/BKLC.php?q=5&n=67&k=11 | 2026-10-19T04:37:24Z | 200 | fd8d8f08f311a35f3046eb294ae86db54c1ce170ab0ccef896aa8dfbe5d66fa4 | lower 39, upper 45 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) |

Compared cell: [66,11] over GF(5). Live lower bound 38, upper bound 45. The certificate excludes d = 45.

cell_excerpt.txt copies the header line and Brouwer lines of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the four neighbouring cells with the offset of the propagation rule (the upper bound implied for the cell is the neighbour upper bound plus the offset).
