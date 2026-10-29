# The record we beat

Snapshot of the four sources the criterion names, for the sorted format (14,15,15), plus this repository's merged
value and pull requests. One plain GET per URL (curl, User-Agent "V3R1T4S-run (curl)"), no cookies, no retries. The
pages themselves are not shipped; fetch_log.txt lists every fetch (time, HTTP status, URL, saved name, sha256, bytes)
and headers/ holds selected response headers of the last fetches.

| source | cell | value | URL | fetched (UTC), HTTP, sha256 |
|---|---|---|---|---|
| fmm_sota.json (createdAt 2026-10-19T20:46:33) | [14, 15, 15] | 1848 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-26T22:30:40Z, 200, 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae |
| Lille per-format page | <14x15x15> | 1890 | https://fmm.univ-lille.fr/14x15x15.html | 2026-10-26T22:30:40Z, 200, 72bedfe2f8cb81f8a2b7ca2daa73561f04f2de1961c52e15dad8bf7c2fe8d465 |
| Lille catalogue index (status_source) | <14x15x15> | 1848 | https://fmm.univ-lille.fr/ | 2026-10-26T22:07:25Z, 200, 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 |
| Perminov docs/ranks.md | 14x15x15 | ZT 1894, Z 1892, Q 1848; min 1848 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-26T22:30:40Z, 200, e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 |
| MerlijnW70/fmm-schemes (git tree, 39 paths, not truncated) | 14x15x15 any orientation | none | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-26T22:30:41Z, 200, f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 |
| this repository, TROPHY_CASE.md entry 44 (merged) | <14,15,15> over Q | 1842 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-26T22:01:21Z, 200, b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |

Minimum over the four named sources: 1848. 1836 is 12 below it, and 6 below the merged 1842.

Pull requests (GitHub search API, all states; the NOVELTY skeptic also read all 755 pull requests): none holds a
(14,15,15) scheme at rank <= 1841. Open pull request #752 (the same contributor's <14,14,15> rank-1709 claim, created
2026-10-25T11:18:58Z) names this rank-1836 scheme as an unclaimed intermediate and ships the code that rebuilds it.
Last searches: 14x15x15 2026-10-26T22:30:41Z, 200, ccbb8c66cc8725a5bf9d9064e102599227f871811e314491d5fc92704aff9ca1; 1836 2026-10-26T22:30:41Z, 200, 39501d448712aab87aa20afd07f9d36eb239c295e48f10f5a5bb6b20afad8189; fmm-catalogue-small-format-rank 2026-10-26T22:30:42Z, 200, 20475ecd0ff8c55e2c39a4d9f562dc7466253e4f7416f931f856bd0ea02815a7.

The skeptics' own fetches (2026-10-26T22:13Z NOVELTY, 22:25Z CRITERION) returned the same sha256 for all four sources;
see panel/novelty.md and panel/criterion.md. TABLE_RECORD.md is the scout's record shown to the panel (unchanged).
The criterion asks for all four sources to be re-fetched immediately before claiming; the last fetch of all four above is 2026-10-26T22:30:40Z.
