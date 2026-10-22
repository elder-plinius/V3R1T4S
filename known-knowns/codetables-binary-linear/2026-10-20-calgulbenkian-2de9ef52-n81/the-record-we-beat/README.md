# The record we beat (metadata only)

One honest GET of the live cell, made by the orchestrator's triage agent. Only the cell excerpt is saved here, not the page.

| Source | URL | UTC fetch time | HTTP | sha256 of the whole page | Extracted cell |
|---|---|---|---|---|---|
| codetables.de QECC cell | https://codetables.de/QECC.php?q=4&n=81&k=63 | 2026-10-20T02:44:48Z | 200 | 91802ff63593ac7484a2835f41979df6571cd3373fa72fe6e191f7dfa5adb3bc | [[81,63]], q=2: lower bound 4, upper bound 6; page says Last change: 10.06.2024 (last modified: 2006-04-03) |

Excerpt saved as `cell_81_63_excerpt.txt`.

Compared cell: qubit stabilizer code [[81,63]]. Live lower bound 4, live upper bound 6. This object: d = 5, strictly above the lower bound and below the upper bound.

The triage agent also fetched the full live quantum table (https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256, 2026-10-20T02:44:12Z, HTTP 200, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6) and compared the neighbouring cells. For this cell, (n,k-1) and (n+1,k) already hold d = 5, while (n-1,k) and (n,k+1) are at most 4 to 5 with lower bound 4; so no one-step rule of the table gives d = 5 for [[81,63]] (triage log live_cmp.log).

Second fetch (the novelty skeptic, same URL): 2026-10-20T02:59:19Z, HTTP 200, page sha256 91802ff63593ac7484a2835f41979df6571cd3373fa72fe6e191f7dfa5adb3bc. Unchanged: lower bound 4, upper bound 6.
