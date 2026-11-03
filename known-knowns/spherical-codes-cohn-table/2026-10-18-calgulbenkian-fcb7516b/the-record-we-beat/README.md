# The record we beat

Each source was fetched once with a plain GET (curl, User-Agent naming V3R1T4S, no retries) by the orchestrator on 2026-11-03; the log line is in the orchestrator's FETCHLOG.txt.

| Source | URL | UTC fetch time | HTTP | sha256 of the full page | Bytes |
|---|---|---|---|---|---|
| plain CSV | https://spherical-codes.org/plain | 2026-11-03T18:04:22Z | 200 | 3a7c9131e9d99c20fdc400eb9d701e628058b5dab162039260495d687fcd6966 | 374688 |
| HTML index | https://spherical-codes.org/ | 2026-11-03T18:04:23Z | 200 | ea628a191fe044704b6a414329a691adc2465d7f60939e9213e7b0f51401578e | 4640837 |

Selected headers were not recorded. Only the compared row is saved here (whole third-party pages are not copied):

- `plain_rows.csv`: the line of /plain for (7, 365), verbatim (columns d,N,cos).
- `index_rows.html`: the table row of the HTML index for (7, 365), verbatim (the row holds the link, the cosine, and the reference cell; a proven-optimal mark would be an ast entity after the link text).

| d | N | /plain cos | star mark in index row | contains 'needs more optimization' | reference cell text |
|---|---|---|---|---|---|
| 7 | 365 | 0.670467238587 | no | no | Antoine Jay, 2026, using the program of A. Jay, M. Poberznik, M. Brut, A. Hemeryck, L.-H. Hoang, M. Gunde, N. Salles, G. Cruchon, and M. Roux, Equidistribution of points on the hypersphere including symmetries, preprint, 2026, doi:0.2139/ssrn.6427919. |

The claim is compared against the /plain cosine (12 decimals) as the bank's criterion states. Codes with more points in dimension 7 were also checked in the same /plain fetch: no row with N > 365 has a cosine at or below this package's value (the nearest, N = 366, reads 0.670923693486).

The package was first filed on 2026-10-18 as a batch of 24 dimension-7 rows (partial win p2), compared against fetches at 2026-10-18T17:39:49Z and 17:50:10Z. By 2026-11-03 the table had superseded 23 of those rows, and the N = 365 row had lost its "needs more optimization" label, so the package was cut down to that row at the maintainer's request. Those earlier fetches are not repeated here.
