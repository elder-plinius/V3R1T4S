# The record we beat

Each source was fetched once with a plain GET (curl, User-Agent naming V3R1T4S, no retries) on 2026-10-18.

| Source | URL | UTC fetch time | HTTP | sha256 of the full page | Bytes |
|---|---|---|---|---|---|
| plain CSV | https://spherical-codes.org/plain | 2026-10-18T17:39:49Z | 200 | 8655466f3692fa9197809db2b6fb7ca4f022b605c08b0fa76d78138915e93f35 | 399047 |
| HTML index | https://spherical-codes.org/ | 2026-10-18T17:39:51Z | 200 | ad3039078a704fe0745f447d29e407554fe3b028fdf8017c617d0c7a80618190 | 4755299 |

No part of either page is copied here. To check against them, fetch both pages yourself (see `../RUN_IT_YOURSELF.md`). The sha256 values above identify the pages as compared on 2026-10-18. The table is maintained, so a later fetch can differ.

| Source | URL | UTC fetch time | HTTP | sha256 of the full page | Bytes |
|---|---|---|---|---|---|
| plain CSV | https://spherical-codes.org/plain | 2026-10-27T13:31:11Z | 200 | 2e6502fa3d8683f6f01a6c22397a6918e77499c22ab32b98c09a48242849a4f0 | 373306 |
| HTML index | https://spherical-codes.org/ | 2026-10-27T13:31:13Z | 200 | 189e750e70f822c66a33de9918a5082c4bd733a01f8ae00e28889dd793a14382 | 4625587 |

The 2026-10-27 fetch is the one the receipt in `../verify-it-yourself/RECEIPTS.md` was run against. The row for (29, 60) is unchanged there (0.032282791684).

Until 2026-10-27 this folder held the verbatim rows as `plain_rows.csv` and `index_rows.html`; the panel reports in `../panel/` refer to them. They were removed at the maintainer's request.

| d | N | /plain cos | star mark in index row | contains 'needs more optimization' | reference cell text |
|---|---|---|---|---|---|
| 29 | 60 | 0.032282791684 | no | no | Ilmari Vahteristo, New spherical codes by tuning an annealing solver, preprint, 2026, arXiv:2610.19988. |

The claim is compared against the /plain cosine (12 decimals) as the bank's criterion states.

## Re-fetch by the panel's novelty skeptic

The novelty skeptic fetched both pages again, each once with a plain GET (curl, honest User-Agent, no retries), and found them byte-identical to the claim's own fetch (same sha256):

| Source | URL | UTC fetch time | HTTP | sha256 of the full page |
|---|---|---|---|---|
| plain CSV | https://spherical-codes.org/plain | 2026-10-18T17:50:10Z | 200 | 8655466f3692fa9197809db2b6fb7ca4f022b605c08b0fa76d78138915e93f35 |
| HTML index | https://spherical-codes.org/ | 2026-10-18T17:50:11Z | 200 | ad3039078a704fe0745f447d29e407554fe3b028fdf8017c617d0c7a80618190 |

Selected headers were not recorded. The pages are not copied here (they are third-party pages).
