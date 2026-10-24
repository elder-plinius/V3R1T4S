# The record we beat (metadata only)

No third-party page is copied here. This claim is compared with what a published paper says about one instance, not with a numerical table. Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries).

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| arXiv abstract page of 2409.03739 (triage fetch) | https://arxiv.org/abs/2409.03739 | 2026-10-19T04:46:03Z | 200 | 070b07ba4ae05a0d8df875e86927d33909e4731ee50ae065792df7d2dfac26d1 | v4 submitted 2026-10-05; the abstract says that for d in {4, 7, 8} the highly symmetric instances can only be solved heuristically |
| arXiv abstract page of 2409.03739 (novelty skeptic) | https://arxiv.org/abs/2409.03739 | 2026-10-19T05:39:14Z | 200 | 070b07ba4ae05a0d8df875e86927d33909e4731ee50ae065792df7d2dfac26d1 | same page, same sha256 |
| arXiv e-print v4 (LaTeX source), triage fetch | https://arxiv.org/e-print/2409.03739v4 | 2026-10-19T04:46:13Z | 200 | 98ba068a9e815b6e9bfa5b2783493f6cc3808e2803c785f16273044b207eefe0 | table of symmetric instances: d = 8, m = 120, root system E8, lower bound 165/109, about 1.5138, marked with an asterisk (heuristic, putative); table of heuristic bounds: d = 8, 120 x 120, 1.51376 against 1.48217 before the paper; table of exact bounds: d = 5, 65 x 385, 1.49339, the largest exact bound for d at least 5 |
| Zenodo record 13693164 (supplementary files of 2409.03739), novelty skeptic | https://zenodo.org/api/records/13693164 | 2026-10-19T05:39:59Z | 200 | 1661a1273766e534a11c302bf1535d07387baf4004f2ead96c4e1d5124f3fac5 | lists d8_n1_120x120.mat, md5 59e20586d208c78d49c73fa9bb99c796, version 0.0.2 of 2024-09-06; the object file here has the same size (239024 bytes) and md5 |
| arXiv 2609.35399v1 (28 Sep 2026), novelty skeptic | https://arxiv.org/pdf/2609.35399v1 | 2026-10-19T05:39:14Z | 200 | edd279e17475265cf7b7a4a21e59a70140da59b944a67f34533ba74c09a46478 | cites 165/109 = 1.513761 as a candidate ratio from the table of 2409.03739 and makes its own bounds conditional on conjectured binary optima; it does not prove the 6104 bound |
| V3R1T4S TROPHY_CASE.md and known-knowns listing, novelty skeptic | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-19T05:37:22Z | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | no Grothendieck entry; no known-knowns folder for this target |

Compared cell: the status of the value 165/109 for the d = 8 instance. The paper prints it as heuristic (1.51376, asterisk); its largest proven bound for d = 8 is 1.49339 (inherited from d = 5 by monotonicity). This package proves the local bound 6104 for the instance, which turns 165/109 into a proven lower bound for K_G(8).
