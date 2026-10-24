# The record we beat (metadata and short excerpts only)

No third-party page is copied here. Every row is one honest GET (curl or equivalent, user agent naming the research client) made on 2026-10-19 (UTC) by the panel's or the contributor's agents; the times, statuses and hashes are copied from their fetch logs, from LITERATURE_ADDENDUM.md and from the panel's reports. LITERATURE_SEARCH.md and LITERATURE_ADDENDUM.md in this folder are the search records written for the loop length 30 claim and copied unchanged. FETCHLOG.txt is the contributor-side builder's fetch log for this claim. The novelty and criterion skeptics repeated and extended the arXiv searches for this claim (panel/novelty.md, panel/criterion.md).

## The bar

Alm's published rigorous upper bound for the connective constant of the 4.8^2 lattice is mu < 1.829254 (J. Phys. A 38 (2005), section 5.1.3: "The matrix G(19, 42), with dimension 125 094, gives the bound mu < 1.829 254"). Jensen's 2004 Table 3 lists the same value rounded as 1.82926. Extracted cell used for comparison: 1.829254.

| Source | URL | UTC fetch time | HTTP | sha256 of the fetched bytes |
|---|---|---|---|---|
| Alm 2005 manuscript copy (Internet Archive copy of the link on Alm's page) | https://web.archive.org/web/2010id_/http://www2.math.uu.se/research/pub/Alm3.pdf | 2026-10-19T06:32:57Z | 200 | a3ddda13eac714eaa6c051dd6a6d57412c1f7b34c79fee86491be6736eb6d7aa |
| Parviainen thesis, full text (Internet Archive copy) | https://web.archive.org/web/2020id_/http://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf | 2026-10-19T06:37:18Z | 200 | 161459735e1fc657a940bdc1dcea85fb6d3137c475f9b5a15c04d1be5620b5f1 |
| Jensen 2004, arXiv abstract page | https://arxiv.org/abs/cond-mat/0409381 | 2026-10-19T05:20:01Z | 200 | 78be1d882fd9d7fae5178b3b59871d23adeec8cf3999730209a22ea4b6a0582a |
| Jensen 2004, ar5iv HTML rendering (bridge definition) | https://ar5iv.labs.arxiv.org/html/cond-mat/0409381 | 2026-10-19T13:49:35Z | 200 | d49b0f2da4ec1b72c38947f62bf9376933bea8e8fc6fa1f8c76dd8678e4c2637 |
| He 2025, arXiv abstract page | https://arxiv.org/abs/2508.01993 | 2026-10-19T05:20:02Z | 200 | 3a3d51f77fc08a5c007ed73b070556b13cea56ea980be401f255b44e211197bc |
| Couronne 2022, arXiv abstract page | https://arxiv.org/abs/2211.16146 | 2026-10-19T05:20:02Z | 200 | 4675536f3843ca111409d86f7448f72dffaf4063b1acc379de2a57bbf1d729b1 |
| Grimmett and Li, Locality of connective constants (builder's fetch) | https://www.statslab.cam.ac.uk/~grg1000/papers/loc-6.pdf | 2026-10-19T15:15:13Z | 200 | 2ec73172d21c51a7a520760009d8e28cf44bc3fbaaea5c8c28a2f1ed70cc46fb |

Fetches made for the loop length 34 panel (novelty skeptic), all HTTP 200 on the first attempt:

| Source | URL | UTC fetch time | HTTP | sha256 of the fetched bytes |
|---|---|---|---|---|
| arXiv API query 1 (connective constant, Archimedean, octagon, 4.8, truncated square) | https://export.arxiv.org/api/query | 2026-10-19T15:51:36Z | 200 | acf4feca8e14a25fe1b28bd043066288a350d74cce40f95eb033159bd9c3bd71 |
| arXiv API query 2 (self-avoiding, upper or rigorous bound, connective constant) | https://export.arxiv.org/api/query | 2026-10-19T15:51:40Z | 200 | e652464a36874903b3d94e6630375d0fd1f85a936f2b17892be05979483845b6 |
| arXiv API query 3 (self-avoiding, finite memory, automaton, transfer matrix, upper bound) | https://export.arxiv.org/api/query | 2026-10-19T15:51:45Z | 200 | 6a6a88c32f9f1827f1bc26c3a569c5bfae1106e6fd0d9d2d62080d96c97f443e |
| arXiv API query 4 (self-avoiding, trapped, pocket, finite component, enclosed, automaton, upper bound) | https://export.arxiv.org/api/query | 2026-10-19T15:51:49Z | 200 | ae83506e8b2a555cdbdd9a7d337df27a05ee140716b3ae99bc227def1f752197 |
| Couronne 2022, arXiv pdf v2 (searched; square lattice only) | https://arxiv.org/pdf/2211.16146v2 | 2026-10-19T15:51:55Z | 200 | 8e3d98d2bdddeed5f23392ab1299e379fba97b670b84a1acaa7408a30db01058 |
| He 2025, arXiv pdf v3 (searched; no 4.8^2 text) | https://arxiv.org/pdf/2508.01993v3 | 2026-10-19T15:51:56Z | 200 | 38bf4354ac1d72b878897bbac04e3b2176c2451780057368b23bc426d7cf8af3 |
| arXiv 2509.04568v1 (searched; square and triangular restricted walks) | https://arxiv.org/pdf/2509.04568v1 | 2026-10-19T15:51:56Z | 200 | 282a4fab2cb56c2e642613ff600290c2d23f12c23634796bc90611167cc0cdca |
| Grimmett and Li (novelty-side re-fetch by the criterion skeptic) | https://www.statslab.cam.ac.uk/~grg1000/papers/loc-6.pdf | 2026-10-19T15:51:57Z | 200 | 2ec73172d21c51a7a520760009d8e28cf44bc3fbaaea5c8c28a2f1ed70cc46fb |
| arXiv 2601.12571v2 (criterion skeptic; no 4.8^2 numeric bound) | https://arxiv.org/pdf/2601.12571v2 | 2026-10-19T16:04:07Z | 200 | d7628862f6454d98bee7fad3329936cbb05de8e6f7a865ca4f7d91a5aaff1566 |

The pull-request check of the novelty skeptic (a read-only search of the repository's pull requests for "4.8", "connective constant" and "self-avoiding" at 2026-10-19T15:52Z) found one pull request, #534, the contributor's own, which this package replaces in place.

## Short quotations

Jensen 2004, Table 3 row, as read by the novelty skeptic of the loop length 32 claim: "(4.82 )   1.804596   1.80883001(6) [15]   1.82926 [3]". Reference [3]: "Alm S E 2004 in preparation. Courtesy of a private communication from R Parviainen and contained in his PhD Thesis ... Uppsala dissertations in mathematics 34".

Alm 2005, summary table row: "(4.82)  3  3  1.804 596 [9]  1.808 830 [12]  1.829 254".

## This claim against the bar

169287/92732 = 1.825551050339. Difference from 1.829254: 3.703e-3. Difference from 1.82926: 3.709e-3.

## Limits of the search

No rigorous 4.8^2 upper bound below 1.829254 was found in Crossref, OpenAlex cited-by lists for Jensen 2004 and Alm 2005, arXiv, or the documents above. Google Scholar, MathSciNet and zbMATH were not searched. See README.md, section Not claimed.
