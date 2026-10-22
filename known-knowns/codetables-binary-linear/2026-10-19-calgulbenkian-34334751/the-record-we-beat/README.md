# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=2&n=161&k=17 | 2026-10-19T04:35:52Z | 200 | 98a2935227b3beaafbf0bc9b556e78dba6d549893b25740b6066d2fc2a32905d | lower 64, upper 72 |
| BKLC neighbour [160,16] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=160&k=16 | 2026-10-19T04:36:55Z | 200 | 348708c9e7abacc53a95daff19fdc2c14bbd28e0693d2786a4000a3bec128459 | lower 65, upper 72 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) |
| BKLC neighbour [160,17] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=160&k=17 | 2026-10-19T04:36:57Z | 200 | 1473ab652e840f016ba1536f38b3667abb0ec0373661d5380b0ea2d81e760a32 | lower 64, upper 71 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) |
| BKLC neighbour [161,16] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=161&k=16 | 2026-10-19T04:36:58Z | 200 | c013894fcc0afa07c88e7ce6e37db1fd8e57f9dc3a3cf5d3fb2d9b93d5a44658 | lower 66, upper 72 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) |
| BKLC neighbour [162,17] | http://www.codetables.de/BKLC/BKLC.php?q=2&n=162&k=17 | 2026-10-19T04:37:02Z | 200 | 04fbb498b8389f15481b0c9d93aade872ff757fd6a3b12608f7359846419ecea | lower 64, upper 72 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) |

Compared cell: [161,17] over GF(2). Live lower bound 64, upper bound 72. The certificate excludes d = 72.

cell_excerpt.txt copies the header line and Brouwer lines of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the four neighbouring cells with the offset of the propagation rule (the upper bound implied for the cell is the neighbour upper bound plus the offset).
