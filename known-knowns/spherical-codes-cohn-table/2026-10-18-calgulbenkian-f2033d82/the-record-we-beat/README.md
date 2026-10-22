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
| 7 | 177 | 0.570051592256 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 178 | 0.570228301539 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 204 | 0.601295919469 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 212 | 0.611962614152 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 215 | 0.614265846451 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 308 | 0.660836744901 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 309 | 0.660912967551 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 310 | 0.660953811794 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 312 | 0.661595420972 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 313 | 0.661974195320 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 314 | 0.662290658947 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 315 | 0.662675365192 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 316 | 0.663332152344 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 317 | 0.663597580717 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 318 | 0.663816385482 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 322 | 0.665029616003 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 323 | 0.665046095133 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 325 | 0.665504583307 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 362 | 0.668965357603 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 364 | 0.670170636995 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 365 | 0.670487284551 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 366 | 0.670943830170 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 367 | 0.671529770134 | no | yes | Henry Cohn, 2026, needs more optimization. |
| 7 | 368 | 0.671589583556 | no | yes | Henry Cohn, 2026, needs more optimization. |

The claim is compared against the /plain cosine (12 decimals) as the bank's criterion states.

## Re-fetch by the panel's novelty skeptic

The novelty skeptic fetched both pages again, each once with a plain GET (curl, honest User-Agent, no retries), and found them byte-identical to the claim's own fetch (same sha256):

| Source | URL | UTC fetch time | HTTP | sha256 of the full page |
|---|---|---|---|---|
| plain CSV | https://spherical-codes.org/plain | 2026-10-18T17:50:10Z | 200 | 8655466f3692fa9197809db2b6fb7ca4f022b605c08b0fa76d78138915e93f35 |
| HTML index | https://spherical-codes.org/ | 2026-10-18T17:50:11Z | 200 | ad3039078a704fe0745f447d29e407554fe3b028fdf8017c617d0c7a80618190 |

Selected headers were not recorded. The whole pages are not copied here (they are third-party pages); the extracted rows are `plain_rows.csv` and `index_rows.html`.
