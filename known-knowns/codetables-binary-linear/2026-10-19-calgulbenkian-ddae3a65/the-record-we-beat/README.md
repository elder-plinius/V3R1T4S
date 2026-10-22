# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=2&n=163&k=18 | 2026-10-19T04:35:55Z | 200 | b747a81b223550784bf9fe377782c47d03c2f1ccbb98f4f8c71f5f8ae744e02a | lower 64, upper 72 |
| BKLC neighbour [162,17] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=162&k=17 | 2026-10-19T04:37:02Z | 200 | 04fbb498b8389f15481b0c9d93aade872ff757fd6a3b12608f7359846419ecea | lower 64, upper 72 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) |
| BKLC neighbour [162,18] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=162&k=18 | 2026-10-19T04:35:54Z | 200 | cb72b55187a09028e182ced0b253b28a3560c40eee8640053a2c15d33378cdd5 | lower 64, upper 72 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) |
| BKLC neighbour [163,17] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=163&k=17 | 2026-10-19T04:37:03Z | 200 | 65652289a445b6e815b869e31cc8533c220599a76a181e26eff1051d1a4ace74 | lower 65, upper 72 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) |
| BKLC neighbour [164,18] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=164&k=18 | 2026-10-19T04:37:05Z | 200 | 52294d46e3a9ee0e6b8deac03b57217671a0a30353bbb6d4c29df6e92b59054d | lower 65, upper 72 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) |

Compared cell: [163,18] over GF(2). Live lower bound 64, upper bound 72. The certificate excludes d = 72.

cell_excerpt.txt copies the header line and Brouwer lines of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the four neighbouring cells with the offset of the propagation rule (the upper bound implied for the cell is the neighbour upper bound plus the offset).
