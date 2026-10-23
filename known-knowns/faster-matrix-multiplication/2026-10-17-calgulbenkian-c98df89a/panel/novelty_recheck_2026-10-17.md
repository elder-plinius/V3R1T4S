# Novelty check: 2x4x7 rank 45, 164 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

All fetches: one plain curl GET, User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Saved copies of the pages are not shipped in this package. Times are UTC, 2026-10-17.

## Primary table and status pages

| Source | URL | Time | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov git tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 01:08:53Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | Not truncated. Exactly one addition_reduced_ZT file for 2x4x7: 2x4x7_m45_cr174_cn308_ZT_reduced.json (cr 174). Minimum cr = 174. |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 01:08:55Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No 2x4x7-45 key (list stops at 4x6x6-116). |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 01:08:56Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | Only 2x4x7 mention is the rank table row (rank 45); no addition count. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 01:08:56Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No 2x4x7 mention. |
| Lille 2x4x7 page | https://fmm.univ-lille.fr/2x4x7.html | 01:08:56Z | 200 | 3d668f206f15825f65def9e7cfe3c4982ddc524817e2f702eb6fd485bbb059d3 | Header "2x4x7:45", scheme taken from AlphaEvolve (Novikov et al., May 2025). No Commentaries section. No addition or operation count cited. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 01:08:57Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row for the 2,4,7 format: "45 Alphaevolve", adds "+308". Its legend defines adds as nz(U)+nz(V)+nz(W) - 2r - n*p, a naive count: not comparable, and higher than 164 in any case. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 01:08:58Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | Entry format [2,4,7], rank 45. Rank 45 is the best known rank, so the eligibility rule holds. |
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 01:08:58Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No 2x4x7 and no matrix-multiplication addition entry. |
| Open pull requests | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 01:08:58Z | 200 | 195c2b0bf35e7ccb9b4fce1d031804aecf133df8ea1043137ff940fe45576c8f | 74 open PRs. For 2x4x7: only #229 (author's own, 169). Other additive-records PRs by others or the author are other formats (#241 3x4x4 124; #218 4x5x6; #205 5x5x5). No competing count for 2x4x7. |
| Merged package listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 01:09:03Z | 200 | 71e39255e834c048eb4e1a619a233c098d629396d86a3b7fa4ec98659dc43fe1 | 46 entries, dated folders plus schemes/; no 2x4x7 or additive-records folder name. |
| Merged package INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 01:09:28Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Seven rows, all rank targets for 13x14x14 to 15x16x16; none is 2x4x7 or an addition count. |
| Issue search "2x4x7" | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+2x4x7&per_page=100 | 01:09:04Z | 200 | 492acd15d39652e0c31c40ae03a002a8a6450d090c85b527f146f5b70efe90de | 2 hits, both the author's own: #11 (closed unmerged 2026-10-14, 164) and #229 (open, 169). No other author. |
| IACR ePrint 2026/849 abstract | https://eprint.iacr.org/2026/849 | 01:09:04Z | 200 | 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b | Title "On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms" (Martensson, Stankovski Wagner). |

Own earlier filings (not competing): PR #11 (closed, same object, 164) and PR #229 (open, different object, 169).

## Papers

- Perminov, arXiv:2512.13365 (https://arxiv.org/pdf/2512.13365, fetched 01:09:39Z, HTTP 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27). Table 1 row for 2x4x7: rank 45, naive 308, GV 181, GP-5 178, GP-40 177, proposed 174. This is the same 174 as his repository file, so it is the count we beat. Its Table 6 (component-wise minima) lists only 4x7x8, 4x8x8, 5x7x8, 6x6x10, 7x7x7, 7x8x8, 8x8x8; 2x4x7 is not among them. Comparable (ternary additions, no basis change), and 174 > 164.
- Perminov, arXiv:2512.21980 (sha256 8187c1ffd0abcb8f729cac3e21b2bca6eb79f371738a4eaf578ea2aab5a33b89): 3x3 only; no 2x4x7 count. Its text only says the method "can be applied to search for optimizations in other small matrix formats".
- Martensson and Stankovski Wagner, IACR ePrint 2026/849 (operator's hand-downloaded text, sha256 99b19def9c130bd95e7dd894fdb4d172b5f87bf5a0344620b2d9c02d9307de60). Scheme code 247-45 appears in two rows. Table 3.3 (all ternary coefficients, over Z, comparable): naive 308, 181, 177. Table 3.6 (all over Z2, not comparable): naive 308, 180, 176. The Table 3.6 caption reads "all over Z2". Table 3.3 caption reads "All schemes have ternary coefficients." Lowest comparable count 177 > 164. Table 3.4 (Z) has no 247-45 row.
- Sun, arXiv:2604.27645 (sha256 0b482e08683fa4be3a48fdde1fb4ad678ec1a9aea77fd5d5ed6fb9641cf35fdf): 3x3 rank 23 only (56 additions); no 2x4x7 count.
- Karunaratne-Idamekorala, arXiv:2607.28676 (sha256 9c5dd27ad71d53932504d7ad6e8f7f3118f6f74631fe7acd2488a98fa003fe38): 3x3 rank 23 only (55); no 2x4x7 count.
- Stapleton-Perminov, arXiv:2609.32388 (sha256 a5b84dba693efff328ce69c1d81934b82952f77e8572020074d78e57548b9e5c): 3x3 rank 23 with an alternative-basis kernel (51); a basis change makes it not comparable, and it has no 2x4x7 count.
- Nielsen, arXiv:2609.06588 (sha256 d2c198bbc8b65c40c43a7f513d102fb3f2e18cef95bbda9aa78e13e8cc4be67c): 3x3 rank 23 only (52). Its abstract says the count is "together with a Karstadt-Schwartz-style basis change", so it is not comparable and has no 2x4x7 count.
- arXiv:2601.05272 (sha256 af31209511b9ad60032a1002dfb35b2df377cfd292b235bd1043c9989509912b): 3x3 only (59 total operations); no 2x4x7 count.
- A general web search for 2x4x7 rank-45 addition counts found only Lille pages that use the rank-45 scheme as a building block; no addition count.

unresolved: arXiv export API search queries (three queries, https://export.arxiv.org/api/query, 01:10:03Z to 01:11:05Z): HTTP 429, 503 and 503, not retried (an earlier http:// attempt returned 301 with an empty body). The literature sweep therefore rests on the named papers plus one web search. The fmm_add_reduction repository (werekorren) and plinopt were not fetched; fmm_add_reduction's results are the baseline in Perminov's Table 1 (its 2x4x7 figure is not shown separately). Plausibility of a comparable count below 164 in these: low, because every published 2x4x7 figure read (174, 177, 178, 181) is above 164.

## Verdict

Full criterion: 164 is strictly below Perminov's live minimum (174, one file, repo and arXiv:2512.13365 Table 1 agree), below the best comparable ePrint 2026/849 count (177 over Z, ternary), and below the COVERAGE.md naive adds (+308, not comparable). Lille page cites no count. Rank 45 equals the best known rank. No competing pull request or merged package covers 2x4x7. Only the author's own #11 (164) and #229 (169) exist.

p1 (3x3x3 rank-23 below 58): not claimed by this object; this object is for 2x4x7. The separate partial-win check, strictly fewer than Perminov's live count for the same format and convention, holds: 164 < 174.

pass: true
