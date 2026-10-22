# The record we beat (metadata and the cells)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator's triage agent on 2026-10-19 (its FETCHLOG.txt). Only the relevant cell or row is copied here, never a whole third-party page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| BKLC cell page | http://www.codetables.de/BKLC/BKLC.php?q=4&n=153&k=7 | 2026-10-19T04:35:50Z | 200 | 71f001d419d57ec63a8fb4c51b7c7d9a5fa891abd59bc50c841e896c614c7ccb | lower 107, upper 111 |
| BKLC neighbour [152,6] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=152&k=6 | 2026-10-19T04:37:13Z | 200 | 0708fb8fc43aa9c161bf1f5ef174c7389dff1d1685f8dc3003c39234b78b7f44 | lower 109, upper 112 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) |
| BKLC neighbour [152,7] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=152&k=7 | 2026-10-19T04:37:14Z | 200 | 26c89db75b34055341ad5fffc77a7004470a7f072199598bb40494378418ea4c | lower 106, upper 110 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) |
| BKLC neighbour [153,6] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=153&k=6 | 2026-10-19T04:37:16Z | 200 | bb924e2ae6a8a0eb1347ce97efbe47dde8d3b5daf17e6e94c8e0fb40cb3b1279 | lower 110, upper 112 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) |
| BKLC neighbour [154,7] | http://www.codetables.de/BKLC/BKLC.php?q=4&n=154&k=7 | 2026-10-19T04:37:18Z | 200 | 8a490a1c419117e77bb942e7896654c99312fbe1fcb7a932cbf81253dee562d6 | lower 108, upper 111 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) |

Compared cell: [153,7] over GF(4). Live lower bound 107, upper bound 111. The certificate excludes d = 111.

cell_excerpt.txt copies the header line and Brouwer lines of the cell page; live_bounds.json holds the two numbers read by verdict.py; neighbours.csv lists the four neighbouring cells with the offset of the propagation rule (the upper bound implied for the cell is the neighbour upper bound plus the offset).
