# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=4&n=148&k=7 | 2026-10-19T04:35:49Z | 200 | fe717030bf07d85ba648d9cdaee69d419745f2d3b65c4f24c93413be36c95254 | lower 103, upper 107 |
| BKLC neighbour [147,6] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=147&k=6 | 2026-10-19T04:37:06Z | 200 | 24d7d8ac0c4ec6318eb4854b3efab342cd32ed9c4abdf38b35baa99d82c932fd | lower 106, upper 108 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) |
| BKLC neighbour [147,7] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=147&k=7 | 2026-10-19T04:37:08Z | 200 | c3ba1cabb0852809cdbc8f3b32169b532f8ca11b2c90286917e3c61d5e411d47 | lower 102, upper 106 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) |
| BKLC neighbour [148,6] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=148&k=6 | 2026-10-19T04:37:10Z | 200 | b5f0e08a333e0e88ca7c1e38499a4438cef448d8be6a6de979e25ad90790cdd2 | lower 106, upper 108 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) |
| BKLC neighbour [149,7] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=149&k=7 | 2026-10-19T04:37:11Z | 200 | fb9cff310e783499d8df38edffd5795c255847d2feedb4dbf0102182039548f6 | lower 104, upper 107 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) |

Compared cell: [148,7] over GF(4). Live lower bound 103, upper bound 107. The certificate excludes d = 107.

cell_excerpt.txt copies the header line and Brouwer lines of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the four neighbouring cells with the offset of the propagation rule (the upper bound implied for the cell is the neighbour upper bound plus the offset).
