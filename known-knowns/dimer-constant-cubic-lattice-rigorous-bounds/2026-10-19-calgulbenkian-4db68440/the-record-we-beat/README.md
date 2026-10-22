# The record we beat

This folder holds the table snapshot metadata: URLs, UTC fetch times, HTTP status and sha256 of each fetched file. The third-party pages themselves are not copied; the extracted cells are quoted below.

Values the claim is compared with, from the orchestrator's triage fetches (2026-10-19) and the builder's own arXiv API queries.

| URL | fetched (UTC) | HTTP | sha256 of the fetched file | note |
|---|---|---|---|---|
| https://arxiv.org/abs/math/0603001 | 2026-10-19T05:30:56Z | 200 | ed796685efcb0dd96f56e94e5b8b0cf343836314c2c26bef69e47e39d260de56 | abstract page |
| https://arxiv.org/src/math/0603001 | 2026-10-19T05:36:22Z | 200 | 1097cf11a7945ea8ac649708cbe39ac0cb70f93257e02bc93f1aa8f4b117d2d9 | LaTeX source archive |
| https://arxiv.org/abs/2607.28810 | 2026-10-19T05:25:59Z | 200 | 9d7fdac30892edc3e69bc9ce086fab732c356d84b27c0c9fd5e8eb2ecafdd1f1 | abstract page; lists v1 (30 Jul 2026) and v2 (11 Aug 2026) only |
| https://export.arxiv.org/api/query?search_query=all:%22monomer-dimer%22+AND+all:%22cubic+lattice%22+AND+all:entropy&sortBy=submittedDate&sortOrder=descending&max_results=15 | 2026-10-19T06:36:44Z | 200 | 35f3f2fffb3911363dc1afbe3f178c528aacc4d9e9b403e1bb886277d6d0744c | arXiv API response (builder fetch) |

Comparator: Friedland, Krop, Lundow and Markstrom, arXiv math/0603001 (v3, 11 Apr 2008), introduction, quoted: "The numerical computations in [FP] yield the best known upper bound $h_3\le 0.7862023450$" and "...we give new lower bounds on $h_d(p)$ which yield the inequality $h_3\ge h_3(0.6814)\ge .7849602275$". [FP] is Friedland and Peled, arXiv math/0402009 (not read). The definitions of h_d and the box limit used in the derivation are in the same source. Excerpt kept in the contributor's workspace and not shipped (third-party text). Margin: 0.7862023450 - 0.7859681 = 2.34e-4 (for the earlier (3,3) claim: 1.58e-4).

The three arXiv API queries (builder fetches, one GET each, honest client) were made to look for a newer or citing paper. `arxiv_api_titles.txt` (shipped here) lists the titles they returned; the full responses are not saved here (sha256 above). Their results: He's paper, Butera et al. (1305.7028), an unrelated 2012 paper, arXiv 1502.06734 (positivity of virial coefficients in lattice dimer models and upper bounds on the number of matchings on graphs; not read) and an unrelated percolation paper. No newer bound on l3 was returned. Abstract of 1502.06734 (read): it studies virial coefficients and states "rigorous upper bounds on N(i) valid for arbitrary graphs and for regular graphs" (N(i) = number of configurations of i dimers); it states no bound on l3, h3 or l4 in the abstract and the body was not read, so whether it yields a Z^4 or Z^3 constant bound is not settled here. The triage agent had no search tool and did not search for citations.
