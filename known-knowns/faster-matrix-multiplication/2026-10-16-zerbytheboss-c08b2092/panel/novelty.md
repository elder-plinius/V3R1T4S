# NOVELTY skeptic

context: subagent (fresh context; saw only this package and kit docs)

verdict: PASS

## Live fetches (2026-10-17T06:16:24Z, single GET each, no retries)

1. `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1` — HTTP 200, sha256 `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab`. Minimum reduced addition count for `2x5x6` at rank 47: **181** (`2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json`, sha256 `7a4e4cf9b1f925b865f97e1b1e1040bc7e91fb3711761fa14be12708be0ec10d`, recounted by `check_slp.py` as `adds_U=40, adds_V=65, adds_W=76, adds_total=181`). Checked `reduced_known.json`, `README.md`, and `CHANGELOG.md`: no count below 181 for `2x5x6` at rank 47.
2. `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` — HTTP 200, sha256 `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`. Lists `[2, 5, 6]` with `"rank": 47`.
3. `https://fmm.univ-lille.fr/2x5x6.html` — HTTP 200, sha256 `30ed5cd77c8c3fc6f41935e706b9d4353bf06b2bcdd8f2c06eac34d97b3f3fd9`. Lists `(2x5x6 : 47)` with no operation-count variant.
4. `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` — HTTP 200, sha256 `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`. Lists naive count `+332`.
5. `TROPHY_CASE.md` and `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` — HTTP 200. Merged PR `#230` claims `<2,5,6>` rank 47 with **179** reduced additions (`38 + 65 + 76`). Our claimed object achieves **177** reduced additions (`38 + 64 + 75`), strictly below both Perminov's live `181` (by 4 additions) and merged PR `#230`'s `179` (by 2 additions).

## Comparison

Claimed: `177` reduced additions (`38 + 64 + 75`) for `<2,5,6>` at rank `47` over `Z` (`object/2x5x6_m47_cr177_ZT_reduced.json`). Live minimum in Perminov: `181` (`177 < 181` strictly).

pass: true
