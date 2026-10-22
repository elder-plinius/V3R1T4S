# The record we beat (metadata only)

No third-party page is copied here. Cell: Erdos problem 757, the upper bound 4/7 for the constant c* (9/17 <= c* <= 4/7, Ma and Tang). This object ties it at 4/7 (it does not go below).

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| erdosproblems.com problem 757 (panel novelty skeptic, most recent) | https://www.erdosproblems.com/757 | 2026-10-18T14:25:04Z | 200 | 0e2f7de764a9423eafe5210cf0d1e6ee8c91125d37f3c98bfdf3a9eb8ca785de | 9/17 <= c <= 4/7 (Ma and Tang); page last edited 10 April 2026 |
| EinsteinArena, Sidon Subsets of (4,5)-Sets (panel novelty skeptic, most recent) | https://einsteinarena.com/problems/sidon-45-set | 2026-10-18T14:25:05Z | 200 | 8aa7ed037111d6a9eac59bc01f82cc9a382698fe45abbe26a0c822a17ba22044 | best ratio 0.571428571 (Ma-Tang, previous SOTA) |
| arXiv 2602.23282 abstract page | https://arxiv.org/abs/2602.23282 | 2026-10-18T14:25:06Z | 200 | e28d7f4e587488ce7d6748db3448109e60937f944b7f6860c2df13472a705155 | the paper's bounds |
| arXiv 2602.23282 HTML (v2, 6 Mar 2026) | https://arxiv.org/html/2602.23282 | 2026-10-18T14:27:27Z | 200 | d1aace4ca6e952deda0f2dbad7336e7e539b74c2e83eaef5a1954c2c1bd6bc29 | Theorem 1.5: c* = lim f(n)/n = inf f(n)/n |

Note on the erdosproblems.com hash: the orchestrator's earlier fetch (2026-10-18T14:04:04Z, HTTP 200, 32200 bytes) has sha256 b5ab477a9e240d10f9dc61845167b3f817175166814165dff5e61827f6077052, which differs from the skeptic's fetch twenty minutes later. Both pages state the same bounds; the cause of the byte difference was not investigated.

The details below are the original record written before the panel (the orchestrator's own fetches).


Cell: Erdos problem 757, upper bound for the constant c in 9/17 <= c <= 4/7, a ratio s(A)/|A| for a (4,5)-set A. This object has ratio 12/21 = 4/7, equal to the live upper bound (not below it).

All rows below are the orchestrator's own fetches (curl, User-Agent naming V3R1T4S, one GET per URL, no retries). The one exception is row 3, which is Argon's saved file and was not fetched by the orchestrator.

| # | What | URL | UTC fetch time | HTTP | bytes | sha256 | Extracted |
|---|---|---|---|---|---|---|---|
| 1 | erdosproblems.com problem 757 | https://www.erdosproblems.com/757 | 2026-10-18T14:04:04Z | 200 | 32200 | b5ab477a9e240d10f9dc61845167b3f817175166814165dff5e61827f6077052 | bounds 9/17 <= c <= 4/7 (Ma and Tang); page status: last edited 10 April 2026. See erdosproblems_757_excerpt.txt |
| 2 | EinsteinArena problem page, Sidon Subsets of (4,5)-Sets (the URL was found in Argon's saved arena listing, row 4) | https://einsteinarena.com/problems/sidon-45-set | 2026-10-18T14:16:41Z | 200 | 31764 | 8aa7ed037111d6a9eac59bc01f82cc9a382698fe45abbe26a0c822a17ba22044 | leaderboard (minimize): 1 Ma-Tang, Previous SOTA, 0.571428571; 2 Hermes-Nous 0.588235294; 3 Wilhelmina 0.600000000; 4 GPT-Explorer 0.615384615. See einsteinarena_excerpt.txt |
| 3 | Argon's saved copy of the arena listing page | https://einsteinarena.com/ | taken by Argon on 2026-10-17 (saved file timestamp 22:38); HTTP status not recorded | | 90780 | 66d51e0ff68b8654e645ff1fd2c6279690c0a0afb947d73b82e46ed74c4ce2a0 | contains the description of this problem: "Improve the 4/7 construction with at most 18 integers. The local-difference condition and largest Sidon subset are computed exactly." |

Notes: the arena problem as described there restricts to at most 18 integers; this object has 21 elements, so it is not an arena-eligible entry. This is stated for the record and no claim about the arena is made. The leaderboard page shows its best ratio as 0.571428571 (4/7).

Compared cell: ratio s/|A|. Reference: 4/7 (0.571428571). This object: 12/21 = 4/7, with |A| = 21 not a multiple of 14.
