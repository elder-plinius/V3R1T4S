# The record we beat

This folder holds the table snapshot metadata: URLs, UTC fetch times, HTTP status and sha256 of each fetched file. The third-party pages themselves are not copied; the extracted cells are quoted below.

Values the claim is compared with, from the orchestrator's triage fetches (2026-10-19) and the builder's own arXiv API queries.

| URL | fetched (UTC) | HTTP | sha256 of the fetched file | note |
|---|---|---|---|---|
| https://arxiv.org/abs/2607.28810 | 2026-10-19T05:25:59Z | 200 | 9d7fdac30892edc3e69bc9ce086fab732c356d84b27c0c9fd5e8eb2ecafdd1f1 | abstract page; lists v1 (30 Jul 2026) and v2 (11 Aug 2026) only |
| https://arxiv.org/src/2607.28810 | 2026-10-19T05:25:59Z | 200 | d913313969df77717b699a76243571e0df490056e06a7fcc0abaf104c6619fd9 | LaTeX source archive (triage log line says only "GET src"; the builder refetched this URL on 2026-10-19T06:49:17Z, HTTP 200, same sha256) |
| https://export.arxiv.org/api/query?search_query=all:%22dimer+constant%22+AND+all:cubic&sortBy=submittedDate&sortOrder=descending&max_results=15 | 2026-10-19T06:36:39Z | 200 | 9a072b085b1b84b9c8d35ff0bd3005bc9f77627a100905122ebaa4161b4558c1 | arXiv API response (builder fetch) |

The record is He's Table 2 itself (rounded upward to six decimals): (2,2) 0.486478; (3,2) 0.471408; (3,3) 0.458558; (4,2) 0.465970; (4,3) 0.457380; (4,4) 0.454673; (5,2) 0.463401; (5,3) 0.454663; (5,4) 0.453365; (5,5) 0.452130; (6,2) 0.462010; (6,3) 0.454618. Section 4 of the source: p = 4 for every entry except (5,5), for which p = 2 was used. Excerpt kept in the contributor's workspace and not shipped (third-party text): `he_2607_28810_excerpt.txt`.

The three arXiv API queries (builder fetches, one GET each, honest client) were made to look for a newer or citing paper. `arxiv_api_titles.txt` (shipped here) lists the titles they returned; the full responses are not saved here (sha256 above). Their results: He's paper, Butera et al. (1305.7028), an unrelated 2012 paper, arXiv 1502.06734 (positivity of virial coefficients in lattice dimer models and upper bounds on the number of matchings on graphs; not read) and an unrelated percolation paper. No newer bound on l3 was returned. Abstract of 1502.06734 (read): it studies virial coefficients and states "rigorous upper bounds on N(i) valid for arbitrary graphs and for regular graphs" (N(i) = number of configurations of i dimers); it states no bound on l3, h3 or l4 in the abstract and the body was not read, so whether it yields a Z^4 or Z^3 constant bound is not settled here. The triage agent had no search tool and did not search for citations.
