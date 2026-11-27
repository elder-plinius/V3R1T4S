# Novelty skeptic: C_4(51), connected quartic graphs on 51 vertices

object: C_4(51) = 152556958807091391617335751728584931970607218791861386 (cell: order 51, connected 4-regular simple graphs)
context: subagent
verdict written: 2026-11-26T02:10:54Z

## Sources (one plain fetch each, no retries, no blocks met)

- https://arxiv.org/abs/2609.31407, fetched 2026-11-26 ~02:09 UTC: Cheng and Xu, "Exact counting of unlabeled quartic graphs by permutation-cycle aggregation". There is only v1 (25 Sep 2026). The abstract gives counts "through order 50". No newer version.
- https://oeis.org/A006820/b006820.txt, ~02:09 UTC: ends at n=28 (a(28)=567437240683788292989). No n=51.
- https://oeis.org/A006820, ~02:09 UTC: b-file n=0..28. Cites arXiv 2609.31407. No terms past 28 and nothing at n=51.
- Release assets: https://zenodo.org/api/records/22961966/versions (the paper's data DOI), ~02:10 UTC: a single version (2026-09-25), titled "Quartic simple graph counts, n = 27–50", with files scripts.zip, src.zip and data.zip. Nothing past order 50.
- Web searches (4), ~02:10 UTC: "number of connected quartic graphs 51 vertices count"; "4-regular graphs enumeration order 51 OR beyond 50 ..."; "Cheng Xu quartic graphs permutation-cycle aggregation order 50 github"; "Meringer genreg House of Graphs quartic graph counts". None found a published count at order 51 or higher. The known frontier is order 50 (Cheng-Xu), then 28 (OEIS), 23 (Xu et al. 2019, arXiv 1907.12455) and 22 (GENREG/Meringer, House of Graphs).
- This repo: TROPHY_CASE.md and known-knowns/ contain no quartic or A006820 entry. Grep hits for "4-regular" occur only in unrelated degree-diameter and code files.
- Pull requests: gh CLI is not installed. Instead I made one plain fetch each of https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+quartic and ?q=is%3Apr+regular-graph-counts-next-order (~02:10 UTC). The only results for this target are #1224 (A002851(21), cubic) and #1225 (A006822(25), degree 6), both open and both in different cells. There is no PR for A006820, C_4 or order 51. The web search may not cover every PR body.

## Comparison
Neighbouring cells: order 50 is published by Cheng-Xu (Table 5 and Zenodo). Order 51 has no published value anywhere I could find, and orders 52 and up have none either. The claim is a first exact value in an empty cell, so this is not a tie with any published value. This panel checks novelty only; whether the value is correct is for the other skeptics.

pass: true
