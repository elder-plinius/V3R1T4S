# Fast Matrix Multiplication Additive Complexity: Format `(2, 4, 7)` (Rank 45) in 164 Additions over `Z`

## What

Explicit exact integer (ring Z) ternary straight-line program in claim/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json (sha256 c98df89a60c52bfd65c3266489f3cbef4a28715305d200e2a3f01334d1076429) for format (2, 4, 7) at best-known rank m = 45 with reduced addition count cr = 164 (U = 27, V = 64, W = 73, fv = 50, cn = 282), symbolically verified across all 3136 bilinear monomials over Z and strictly beating Perminov addition_reduced_ZT (174 in 2x4x7_m45_cr174_cn308_ZT_reduced.json, margin -10), reduced_known.json (none), README.md/CHANGELOG.md (no lower count), fmm.univ-lille.fr/2x4x7.html (no complexity variant listed), and matmulcatalog COVERAGE.md adds (+308).

In this package, the straight-line program file is stored at `object/2x4x7_m45_cr164_fv50_cn282_ZT_reduced.json` (identical bytes, SHA-256 `c98df89a60c52bfd65c3266489f3cbef4a28715305d200e2a3f01334d1076429`, 20,225 bytes).

## Check it yourself

From this package folder (`2026-10-17-calgulbenkian-c98df89a/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` (3.8+, standard library only).
- **Rough laptop time**: < 1 second.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

All criterion sources were fetched live on `2026-10-14` (`03:50:15Z`-`03:50:28Z`, one honest GET per source, no retries; see `the-record-we-beat/README.md` and `the-record-we-beat/sources_2026-10-14T03-50-16Z.json`):

| Source | Cell | Rank `m` | Listed Additions (`cr`) | Our Additions (`cr`) | Margin | URL | UTC Fetch Time |
|---|---|---|---|---|---|---|---|
| Perminov `addition_reduced_ZT` | `2x4x7_m45` | `45` | `174` (`2x4x7_m45_cr174_cn308_ZT_reduced.json`) | **`164`** | **`-10`** | `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT` | `2026-10-14T03:50:16Z` |
| Perminov `reduced_known.json` | `2x4x7-45` | `45` | `none` | **`164`** | — | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json` | `2026-10-14T03:50:15Z` |
| Sedoglavic `fmm_sota.json` | `[2, 4, 7]` | `45` | — (rank `45` verified) | **`164`** | — | `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` | `2026-10-14T03:50:16Z` |
| Lille per-format catalogue | `2x4x7` | `45` | none | **`164`** | — | `https://fmm.univ-lille.fr/2x4x7.html` | `2026-10-14T03:50:20Z` |
| `solven-eu/matmulcatalog` `COVERAGE.md` | `2,4,7` | `45` | `+308` (naive) | **`164`** | — | `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` | `2026-10-14T03:50:17Z` |

Re-checked on `2026-10-17` before refiling (one honest GET per source, no retries; full report in `panel/novelty_recheck_2026-10-17.md`, a fresh-context novelty skeptic):

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live tree) | 2x4x7 rank 45 | 174 (one file, `2x4x7_m45_cr174_cn308_ZT_reduced.json`); unchanged | 164 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-17T01:08:53Z |
| Perminov, arXiv:2512.13365, Table 1 | 2x4x7 rank 45 | 174 | 164 | https://arxiv.org/abs/2512.13365 | 2026-10-17 |
| fmm_sota.json (Sedoglavic), best known rank | 2x4x7 | rank 45 (eligibility) | rank 45 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-17T01:08:58Z |
| Lille per-format page | 2x4x7 | rank 45; no addition or operation count cited | 164 | https://fmm.univ-lille.fr/2x4x7.html | 2026-10-17T01:08:56Z |
| matmulcatalog COVERAGE.md, adds column | 2x4x7 | +308, a naive count, not comparable | 164 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-17T01:08:57Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 2x4x7 rank 45 | lowest count listed for 247-45: 177 over Z (Table 3.3); 176 over Z2 (Table 3.6, not comparable); author's reading of a hand-downloaded PDF | 164 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S open pull requests and issue search | 2x4x7 | only the author's own #11 (this object) and #229 (169) | 164 | https://github.com/elder-plinius/V3R1T4S | 2026-10-17T01:09:04Z |

## Not claimed

- This result reduces the number of straight-line program additions/subtractions (`cr = 164` vs `174`) over $\mathbb{Z}$ at the existing best-known bilinear rank `m = 45`; it does not lower the multiplicative rank `m`.
- Checked internally by three independent skeptic subagents (`panel/`) and the standalone symbolic checker shipped here; not peer reviewed.

## Filing history

- This object was first filed as pull request #11 on 2026-10-14. #11 was closed unmerged the same day together with about thirty other early pull requests during a handoff between the contributor's sessions, not for a defect.
- Pull request #229 (2026-10-16) filed a different object for this cell at 169 additions. On 2026-10-17 the maintainer checked this 164 object independently (exact over Z, U 27, V 64, W 73) and asked for it to be filed instead; this package replaces the 169 package in #229.
- The scheme is not the one in Perminov's file: a rank-preserving ternary flip-graph walk from his rank-45 scheme gives naive count 282 (his file: 308), and CSE then gives 164 reduced additions.

## Credits

- **A. I. Perminov**, *FastMatrixMultiplication* and *ternary_addition_reducer* (`https://github.com/dronperminov/FastMatrixMultiplication`, `https://github.com/dronperminov/ternary_addition_reducer`, arXiv:2512.13365, arXiv:2512.21980, arXiv:2606.02480): our straight-line program builds directly on Perminov's ternary scheme for `2x4x7` (`m = 45`).
- **A. Sedoglavic**, *Catalogue of Fast Matrix Multiplication Algorithms* (`https://fmm.univ-lille.fr/` and `https://github.com/sedoglavic/fmm_digest`).
- **solven-eu**, *matmulcatalog* (`https://github.com/solven-eu/matmulcatalog`).
- Contributor credit: `calgulbenkian`.
