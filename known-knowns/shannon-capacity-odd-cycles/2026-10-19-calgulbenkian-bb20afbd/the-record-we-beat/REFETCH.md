# Re-fetch before checking this package

Two live records were fetched again once each, immediately before check_run was run on this package (plain GET with a User-Agent naming V3R1T4S). Both were byte-identical (same sha256) to the panel's fetches of 2026-10-20T03:14Z and to the version the third criterion skeptic saw at 2026-10-20T04:46Z, so neither had moved.

| Source | URL | UTC fetch time | HTTP | sha256 |
|---|---|---|---|---|
| 9a.md (primary table) | https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/9a.md | 2026-10-20T04:53:02Z | 200 | 92f6e1ee5d7219af29572c37dbb54192f3d12c2b1bc818aaf1c3e4ffe46d9899 |
| Tandon abstract page | https://arxiv.org/abs/2608.30273 | 2026-10-20T04:53:03Z | 200 | 08530da3c5da68909805805a5a8f4863bee2c7c75c1cb799bb66c80e01db7224 |

The value this claim is compared against: Theta(C_7) >= 3.25883262035326630912153905181047543760538759432195 (Tandon, d = 500, top entry of 9a.md). Records for this constant move every few weeks; re-fetch before relying on this comparison.
