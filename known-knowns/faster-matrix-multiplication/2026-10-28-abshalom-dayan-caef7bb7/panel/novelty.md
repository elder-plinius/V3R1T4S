context: subagent (fresh Claude Code Agent context, Opus 5.5, saw only claim/)

# Novelty skeptic: fmm-catalogue-small-format-rank, <14,15,13> (sorted <13,14,15>) rank 1644 over Q

Claim read: claim/CLAIM.md, claim/TABLE_RECORD.md, header of claim/object/u.txt ("format 14 15 13", "rank 1644"; each
factor file has 1649 lines = 5 header lines + 1644 terms). Rank is invariant under permuting the three dimensions, so
the cell is the sorted format (13,14,15) and every permutation of it.

## Live sources (one plain curl GET each, User-Agent "V3R1T4S-panel (curl)", no cookies, no retries)

Bodies saved in the workspace under fetch/. Times are UTC from `date -u` taken immediately before each request.

| source | UTC time | HTTP | sha256 of body | value for (13,14,15), any permutation |
|---|---|---|---|---|
| https://fmm.univ-lille.fr/ (status_source, catalogue index) | 2026-10-28T22:16:24Z | 200 | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row id="13x14x15": "&lang;13&times;14&times;15:1681&rang;", rank column 1681, naive 2730, credit "Perminov 2026". No row id for any other permutation (index lists sorted formats only). |
| https://fmm.univ-lille.fr/13x14x15.html | 2026-10-28T22:16:24Z | 200 | d2a562a11c213effc7df98468757cda923925f248fab408ed38c485039851158 | "&lang;13&times;14&times;15:1681&rang;" (twice); the only number in 1600..1700 on the page is 1681 |
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-28T22:16:25Z | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | {'format': [13, 14, 15], 'rank': 1681, 'exponent': 2.816137}; only entry whose sorted format is (13,14,15); createdAt 2026-10-19T20:46:33 |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-28T22:16:25Z | 200 | 5f433497fdc4ea056f0d13e5adfdb22b70237ea23170134fe1a3d9637bb5f4bb | line 674: "`13x14x15` \|  1681 (?)   \| 1681 (1714)  \| 1681 (1714)  \|   2.816136526"; min over ZT/Z/Q = 1681; no other permutation row |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-28T22:16:25Z | 200 | 52db72a9cd408815d98ebcd851d55fb13b8d84eaa70b7ebd7c4de67cc29b9e61 | no 13x14x15 entry (links to docs/ranks.md and docs/results.md) |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/results.md | 2026-10-28T22:19:25Z | 200 | bb39a4a91f34a4cc49a5a391f23c980f08b2f80c0e2ef0ac40c3114ecfa69c1e | line 258: "`13x14x15` \|  1714 (`Z`) \| 1681 (ZT/Z) ..." -> 1681 |
| https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS | 2026-10-28T22:16:26Z | 200 | de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd | 31 scheme files, none for any permutation of 13x14x15 (nearest: 13x13x15_m1591, 13x14x16_m1805) |
| https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-28T22:16:26Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | truncated False, 39 entries; no path containing 13, 14 and 15 -> no entry |
| https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (context; GF(2) clause) | 2026-10-28T22:16:26Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | line 620: "⟨13,14,15⟩ ... 1681 in F₂, R/Q/Z" |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-28T22:16:26Z | 200 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 | row 48: <13,14,15> 1677, "superseded 2026-10-15 by contributed rank 1645, pull request #166" |
| https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1 (literature) | 2026-10-28T22:19:21Z | 200 | d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339 | truncated False, 31 entries; no rectangular format at all; only cube files (incl. schemes/15x15x15_r1977.npz) |

Minimum over the four criterion sources: **1681**. My hashes for every non-API source and the MerlijnW70 tree match the
ones in claim/TABLE_RECORD.md byte for byte.

## Pull requests of elder-plinius/V3R1T4S (all states)

Pulls list API, https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N, one request at
a time, about 5 s apart, 2026-10-28T22:17:24Z to 22:17:59Z, pages 1-8 all HTTP 200 (100,100,100,100,100,100,100,81
entries). **781 PRs read, all distinct, numbers 1 to 811.** Search API not used.

Scan of every title and body: strict regex for every permutation of 13/14/15 joined by x, ×, *, comma, &times;,
\times or "by" (with optional spaces), plus a looser pass (any three of 13/14/15 within 8 non-digit characters).
Hits (identical set from both passes):

| PR | state | what it is | rank stated for (13,14,15) |
|---|---|---|---|
| #4 | closed, not merged | "[claim] ... format (13, 14, 15) rank 1646 over Q (beats 1681 bar)" | 1646 |
| #164 | merged | (13,13,14) rank 1479; 13x14x15 named only as an intermediate cut in the LITA chain | none stated |
| #166 | merged | "[claim] ... (13, 14, 15) rank 1645 over Q (beats 1677)" | 1645 |
| #177 | merged | (13,13,15) rank 1578; 13x14x15 named only as an intermediate cut | none stated |
| #743, #747, #749, #751 | open | partial-win p1 claims for <22,23,23>, <26,27,27>, <28,29,29>, <30,31,31>; "13,14,15" occurs only inside index lists [0,1,...,21] | not a format mention |
| #809 | open | card-guessing exact rationals, "n = 11, 12, 13, 14, 15, 16" | not a format mention |

"1644" occurs only in #55 (inside a sha256 hex string) and #399 (inside "16448 rows" of a spherical-codes count); neither
concerns matrix multiplication. **No PR, open or closed, claims rank <= 1644 for any permutation of (13,14,15).**

## TROPHY_CASE.md and known-knowns (pinned copy, commit c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8, 2026-10-27)

- Pinned TROPHY_CASE.md sha256 83af764f...6113 equals the live one fetched above. Row 48: <13,14,15> rank 1677 over Q,
  superseded 2026-10-15 by the contributed rank 1645 (PR #166). Summary row line 15 says the same.
- known-knowns/faster-matrix-multiplication/INDEX.csv and README.md list our own 13x14x15 at 1677;
  the contributed folder 2026-10-15-anonymous-c6d1e0ab-49ee1c4f holds object/13x14x15_r1645_Q.json, sha256
  49ee1c4f6642d1245e5af697eeb2f342024d04f06a0cc9113501ce8f45177144, identical to claim/the-record-we-beat/13x14x15_r1645_Q.json.
- Other merged folders name 13x14x15 intermediates only at rank 1645 (folder 4b613512, parent of its 13x14x14 r1538) and
  1649 (folders e738d0f3 and 9a8f254e). The only "1644" near 13x14x15 in the repository is the 1645 package's negative
  control (last term deleted, reported as FAIL). Nothing merged is at or below 1644.
- kit/POLICY.md "Fast matrix multiplication" rule 1: compare with Perminov's README/docs/ranks.md, what is merged here,
  and published literature. Merged value: **1645**.

## Literature (last 24 months)

- LITA repository (khoruzhii/lita): cubes only, no rectangular schemes (tree above).
- Two web searches ("13x14x15" matrix multiplication rank; flip-graph rectangular formats up to 16, 2026) and one on the
  LITA authors. Relevant items: Perminov, arXiv:2603.02398 (March 2026, open-source flip-graph framework, 680 formats up
  to 16x16x16) and arXiv:2606.02480 (June 2026, meta flip graph + serendipitous product, 207 formats improved); their
  ranks feed Perminov's docs/ranks.md, which lists 1681 for 13x14x15. Also Kauers-Wood arXiv:2510.19787 (meta flip graph,
  around thirty formats) and arXiv:2511.20317 (ternary meta flip graph), neither giving 13x14x15 below 1681 in what I
  read. Search results also surfaced the Lille 13x14x15 page (1681). I read only search snippets and abstracts, not the
  full papers' tables. No published rank <= 1644 for any permutation of (13,14,15) found.
- matmulcatalog COVERAGE.md: 1681 (F2 and R/Q/Z).

## Blocks

None. Every request returned HTTP 200; no tool-guard or classifier block.

text addressed to reviewers: none found (simple scan of all 781 PR titles and bodies and the claim's markdown files for
such text; no hits).

## Verdict

| comparator | value |
|---|---|
| fmm_sota.json | 1681 |
| Lille per-format page / index row | 1681 / 1681 |
| Perminov docs/ranks.md min(ZT, Z, Q) | 1681 |
| MerlijnW70/fmm-schemes | no entry |
| merged in V3R1T4S (PR #166; TROPHY_CASE row 48 supersession) | 1645 |
| any V3R1T4S PR, any state | lowest 1645 (#166); #4 is 1646 |
| literature found | nothing below 1681 |
| **claim** | **1644** |

1644 is strictly below every value I could read: 37 below the four-source minimum 1681 and 1 below the merged 1645. It
is not a tie. Novelty holds for rank only, over Q; I checked novelty only, not correctness of the scheme (another
skeptic covers that). The margin over this repository's own merged value is one term.

novelty: CONFIRMED (1644 < 1645 merged < 1681 four-source minimum)

pass: true
