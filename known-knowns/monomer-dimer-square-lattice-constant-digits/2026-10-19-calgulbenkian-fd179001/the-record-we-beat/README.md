# Table record (metadata and short excerpts only)

Each row is one honest GET (curl, user agent naming the research client, no retries) made by the contributor's team on 2026-10-19 (UTC), copied from the contributor's FETCHLOG. No page is copied here, only the quotations below.

| Source | URL | UTC fetch time | HTTP | sha256 of the fetched bytes |
|---|---|---|---|---|
| Friedland and Peled, arXiv math/0402009 (pdf) | https://arxiv.org/pdf/math/0402009 | 2026-10-19T03:44:36Z | 200 | 1af5cabb56db8adb88bde2764ff72771b4a2cc489f19d81dcfd61501bec3ac5a |
| Kong, arXiv cond-mat/0610690 (pdf) | https://arxiv.org/pdf/cond-mat/0610690 | 2026-10-19T03:44:36Z | 200 | d10ead0e8871b848859c7dc600f3754ebeb90c498807ac5c5e263867d16f73f7 |
| Finch, arXiv 2001.00578 (abstract page only) | https://arxiv.org/abs/2001.00578 | 2026-10-19T03:57:22Z | 200 | 291e444f5a7b42aef517a01657e4b18bb8197ec2acad246f27364fcf28280e9c |
| Butera, Federbush and Pernici, arXiv 1305.7028 (pdf) | https://arxiv.org/pdf/1305.7028 | 2026-10-19T03:57:23Z | 200 | 56b998f520959c8f4d640d19c521804e215cd6153e87e96387ba09ad9577fa8f |
| arXiv API query, all:"monomer-dimer" AND all:entropy, 30 most recent | http://export.arxiv.org/api/query?search_query=all:%22monomer-dimer%22+AND+all:entropy&max_results=30&sortBy=submittedDate&sortOrder=descending | 2026-10-19T03:57:24Z | 200 | d6cdd10fc1c91a75502671d4b2291eaf639f9191fb837f256a372eef7d279015 |
| OEIS search for the digits 6627989728337 (json) | https://oeis.org/search?q=6627989728337&fmt=json | 2026-10-19T04:02:26Z | 200 | 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b |
| OEIS search for the digits 1940215351483 (json) | https://oeis.org/search?q=1940215351483&fmt=json | 2026-10-19T04:02:26Z | 200 | 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b |

## Comparator values (short quotations)

**Friedland and Peled** (Adv. Appl. Math. 34 (2005), arXiv math/0402009; text extracted from the fetched pdf, section 8): "Hence we obtain the value h2 = .66279897, correct to 8 decimal digits." From the abstract: "we compute the monomer-dimer constant for the 2-dimensional grid to 8 decimal digits". Certified decimals taken as the comparator: 8.

**Kong** (Phys. Rev. E 74, 061102 (2006), arXiv cond-mat/0610690): "The function f2 (rho) reaches the maximum value f2 (rho*) = 0.662798972834 at rho* = 0.6381231, with 11 correct digits." Its bracket: "0.662798972831 < f2 (rho*) < 0.662798972845, ... where the value of f_inf,n (rho) for n = 16 is used as the upper bounds, and that for n = 17 as the lower bounds." The bank and the contributor's report take the published decimals as 12 (the printed 0.662798972834) and the stated accuracy as 11 correct digits. Rigor: the paper's bracket ends are numerical cylinder values; the contributor's report notes that it did not check whether the paper proves the lower end.

**Butera, Federbush and Pernici** (arXiv 1305.7028): "For d = 2 in the case of h_d, this lower bound 0.662798966, is smaller than the estimate 0.662798972(1) obtained in Ref.[19] by Pade approximants." Estimate with about 9 decimals plus one uncertain digit.

**Finch** (arXiv 2001.00578): only the abstract page was fetched; the bank text says it quotes 0.66279897 only. This was not independently confirmed from the fetched page.

**Searches** (single GET each, no retries, results as fetched): the two OEIS digit searches (6627989728337 and 1940215351483) returned an empty result (the response has the same 4-byte body and the same sha256 for both). The arXiv API query for monomer-dimer and entropy (30 most recent) was fetched; its result list is not copied here. These are one-shot searches, not a proof of absence; no general web or Google Scholar search was made.
