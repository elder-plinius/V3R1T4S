# The record we compare against (metadata and one saved row)

Two honest GETs (curl, User-Agent naming V3R1T4S, no retries): the live table of 2026-11-17, which is the one this claim is compared with, and the first fetch of 2026-10-19, kept below as an earlier snapshot.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Live table (current): dobbelaere_extended.html | https://bertdobbelaere.github.io/sorting_networks_extended.html | 2026-11-17T17:41:47Z | 200 | b0e87a7df41391d63fcc2b00be41e23e1c52c2667962154c935fd8953405d4e5 | row n = 53: 53 (410, 23) (411, 22) (412, 21) (414, 20) (423, 19) 285…410 11…19 Size ubound: SorterHunter, depth ubound: Batcher odd-even merge . The page states: Page updated on Sun Nov 8 16:24:50 2026. |
| Earlier snapshot (2026-10-19; superseded by the live row above): dobbelaere_extended.html | https://bertdobbelaere.github.io/sorting_networks_extended.html | 2026-10-19T04:32:30Z | 200 | 5515e5d7862caaf31058225ff215850c1987704f6bcd9b5920590e2478d41a53 | row n = 53: 53 (411, 22) (412, 21) (414, 20) (423, 19) 285…411 11…19 Size ubound: Van Voorhis (4,4) merge, depth ubound: Batcher odd-even merge . |

Saved excerpt: the-record-we-beat/listed.json (row text and the listed (size, depth) pairs of the live table; the 2026-10-19 row is kept inside it under `earlier_snapshot`). The earlier snapshot's page stated: updated on Tue Oct 13 20:10:24 2026.

Compared cell: n = 53, (size, depth) = (413, 20) against the live listed pairs (410, 23), (411, 22), (412, 21), (414, 20), (423, 19). (On the 2026-10-19 snapshot the listed pairs were (411, 22), (412, 21), (414, 20), (423, 19); the live table adds (410, 23).)
