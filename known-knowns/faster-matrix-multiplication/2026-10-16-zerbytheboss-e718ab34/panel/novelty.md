# NOVELTY skeptic

context: subagent (fresh context; saw only this package and kit docs)

verdict: PASS

## Live fetches (2026-10-17T05:18:50Z–05:18:53Z, single GET each, no retries)

1. `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1` — HTTP 200, sha256 `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab`. Under `schemes/results/addition_reduced_ZT/` there is a single file matching `2x4x7` (or any permutation `2x7x4`, `4x2x7`, `4x7x2`, `7x2x4`, `7x4x2`):
   - `2x4x7_m45_cr174_cn308_ZT_reduced.json` (rank 45, cr = 174).
   Minimum reduced addition count at rank 45: **174**. Fetched `2x4x7_m45_cr174_cn308_ZT_reduced.json` (HTTP 200, sha256 `b839eb6e30cfd9e0b045d249dfdacfd832ad2d7a5770f6a8d88c29f6ff486e84`) and ran `verify-it-yourself/check_slp.py`: `adds_U=35, adds_V=69, adds_W=70, adds_total=174, VALID=True`.
   Also checked `reduced_known.json` (HTTP 200, sha256 `ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`; no `2x4x7` entry), `README.md` (sha256 `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`), and `CHANGELOG.md` (sha256 `07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175`): no count below 174 for `2x4x7` at rank 45.
2. `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` — HTTP 200, sha256 `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`. Entry `[2, 4, 7]`: `"rank": 45`.
3. `https://fmm.univ-lille.fr/2x4x7.html` — HTTP 200, sha256 `3d668f206f15825f65def9e7cfe3c4982ddc524817e2f702eb6fd485bbb059d3`. Lists `(2x4x7 : 45)` citing AlphaEvolve (Novikov et al., May 2025, `arXiv:2506.13131`), with no operation-count variant.
4. `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` — HTTP 200, sha256 `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`. Row `2x4x7 | 56 | 45 (-20%) | - | +308`. The `+308` is the naive count.
5. `TROPHY_CASE.md` and `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` — HTTP 200. Open PR `#229` claims `<2,4,7>` rank 45 with **169** reduced additions, and withdrawn PR `#11` (verified valid by maintainers) reports **164** reduced additions. In PR `#241`, the maintainer noted that our `<2,4,7>` result is below `#229` and invited us to file it as its own package. Our claimed object has **161** reduced additions (`U 35 + V 58 + W 68 = 161`), which is strictly below Perminov's live `174` (by 13 additions), open PR `#229`'s `169` (by 8 additions), and withdrawn PR `#11`'s `164` (by 3 additions).

## Literature check (last 24 months)

Checked AlphaEvolve (Novikov et al., `arXiv:2506.13131`, May 2025), Dumas, Pernet & Sedoglavic (`arXiv:2511.10591`, Nov 2025, `3x3`), Moosbauer & Poole (`arXiv:2502.04514`, Feb 2025), and Mårtensson & Wagner (`ePrint 2026/849`; PDF behind an interactive challenge page, noted in `README.md`). None reports a `<2,4,7>` rank-45 straight-line program with 161 or fewer additions.

## Comparison

Claimed: `161` reduced additions (`35 + 58 + 68`) for `<2,4,7>` at rank `45` over `Z` (`object/2x4x7_m45_cr161_ZT_reduced.json`). Live minimum across Perminov (`174`), Lille (none), `COVERAGE.md` (`308` naive), open PR `#229` (`169`), and withdrawn PR `#11` (`164`): `161 < 164 < 169 < 174` strictly.

pass: true
