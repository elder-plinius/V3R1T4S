# The record we beat

Each source was fetched once with a plain GET (curl, User-Agent naming V3R1T4S, no retries) by the orchestrator on 2026-10-18; the log line is in the orchestrator's FETCHLOG.txt.

| Source | URL | UTC fetch time | HTTP | sha256 of the full page | Bytes |
|---|---|---|---|---|---|
| plain CSV | https://spherical-codes.org/plain | 2026-10-18T17:39:49Z | 200 | 8655466f3692fa9197809db2b6fb7ca4f022b605c08b0fa76d78138915e93f35 | 399047 |
| HTML index | https://spherical-codes.org/ | 2026-10-18T17:39:51Z | 200 | ad3039078a704fe0745f447d29e407554fe3b028fdf8017c617d0c7a80618190 | 4755299 |

Only the relevant rows are saved here (whole third-party pages are not copied):

- `plain_rows.csv`: the line(s) of /plain for the compared (d,N), verbatim (columns d,N,cos[,minimal polynomial]).
- `index_rows.html`: the table row(s) of the HTML index for the compared (d,N), verbatim (the row holds the link, the cosine, and the reference cell; a proven-optimal mark would be an ast entity after the link text).

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

Selected headers were not recorded. The whole pages are not copied here (they are third-party pages); the extracted rows are `plain_rows.csv` and `index_rows.html`.
