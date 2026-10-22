# The record we beat

This folder holds the table snapshot metadata: URLs, UTC fetch times, HTTP status and sha256 of each fetched file. The third-party pages themselves are not copied; the extracted cells are quoted below.

Values the claim is compared with, from the orchestrator's triage fetches (2026-10-19) and the builder's own arXiv API queries.

| URL | fetched (UTC) | HTTP | sha256 of the fetched file | note |
|---|---|---|---|---|
| https://arxiv.org/abs/1305.7028 | 2026-10-19T05:30:57Z | 200 | 2410d8f8bf5e997bfb4ecf38bfaef624d84dd57dad7d2255fa9a099b75135a21 | abstract page |
| https://arxiv.org/src/1305.7028 | 2026-10-19T05:39:44Z | 200 | 77c959e838e6a19dbccae2f26eeb246efc005e22943cd53618aa755ddedb52cc | LaTeX source archive |
| https://export.arxiv.org/api/query?search_query=all:dimer+AND+all:hypercubic+AND+all:%22upper+bound%22&sortBy=submittedDate&sortOrder=descending&max_results=15 | 2026-10-19T06:36:49Z | 200 | 404b0c9e6dbb13fbf28b4018e9c856f76ba6a35c86152884e353a89eaced37bf | arXiv API response (builder fetch) |
| https://arxiv.org/abs/1502.06734 | 2026-10-19T06:49:22Z | 200 | e109061119d0e7fea15e3b7715d14a0a69a2d1b3afcc11062c46660d10f7051d | abstract page of Positivity of the virial coefficients in lattice dimer models and upper bounds on the number of matchings on graphs (builder fetch) |

Comparator: Butera, Federbush and Pernici, arXiv 1305.7028 (Phys. Rev. E 88, 032113), the table of rigorous bounds (label tab3 in the source; Argon calls it Table III), row lambda_4(1): lower bound 0.53972077, upper bound 0.66278769, with the caption's rigorous bounds (1/2) ln(2d) - 1/2 <= lambda_d(1) <= ln((2d)!)/4d, citing P. Federbush and S. Friedland, J. Stat. Phys. 143, 306 (2011). Note: Argon's pre-registration quotes a Z^4 lower bound 0.55808612 attributed to Schrijver 1998 and this table; the table lists 0.53972077. Excerpt kept in the contributor's workspace and not shipped (third-party text): `bfp_1305_7028_excerpt.txt`. Margin: 0.66278769 - 0.584015 = 0.0788.

The three arXiv API queries (builder fetches, one GET each, honest client) were made to look for a newer or citing paper. `arxiv_api_titles.txt` (shipped here) lists the titles they returned; the full responses are not saved here (sha256 above). Their results: He's paper, Butera et al. (1305.7028), an unrelated 2012 paper, arXiv 1502.06734 (positivity of virial coefficients in lattice dimer models and upper bounds on the number of matchings on graphs; not read) and an unrelated percolation paper. No newer bound on l3 was returned. Abstract of 1502.06734 (read): it studies virial coefficients and states "rigorous upper bounds on N(i) valid for arbitrary graphs and for regular graphs" (N(i) = number of configurations of i dimers); it states no bound on l3, h3 or l4 in the abstract and the body was not read, so whether it yields a Z^4 or Z^3 constant bound is not settled here. The triage agent had no search tool and did not search for citations.
