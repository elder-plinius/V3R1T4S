context: subagent (fresh Claude Code Agent context, Opus 5.5, saw only claim/)

# Criterion skeptic: fmm-catalogue-small-format-rank, claimed rank 1644 for <14,15,13> (sorted (13,14,15))

Bottom line: the object meets the main success criterion literally. It is an exact rational scheme with 1644
rank-one terms. Each of the four named sources, re-fetched by me, gives 1681 for (13,14,15), and the value merged in
this repository (POLICY rule 1) is 1645. No partial win is needed or claimed.

## 1. Criterion text matches the bank

A one-off script (work/cmp.py in my workspace) loaded repo/bank/targets.json, took the entry with id
`fmm-catalogue-small-format-rank` and compared its `success_criterion` with the block under "Success criterion
(verbatim from the bank)" in claim/CLAIM.md. Output: `equal: True 1571 1571`. Both partial-win statements also
compare equal (`partials equal: [True, True]`). Pinned repo commit c027ca3e0c8d (2026-10-27T09:42:35-07:00).

## 2. Clause by clause

| clause | verdict | evidence |
|---|---|---|
| explicit bilinear scheme (U, V, W or list of rank-one terms) | met | object/u.txt, v.txt, w.txt: one line per term, sparse index:coefficient, 1644 lines each |
| max(n,m,p) <= 16 | met | format 14 15 13, max 15 |
| sorted format not (3,3,3) or (4,4,4) | met | sorted (13,14,15) |
| r strictly below fmm_sota.json | met | live entry {"format": [13, 14, 15], "rank": 1681}; 1644 < 1681 |
| r strictly below Lille per-format page (13x14x15.html) | met | page has "13&times;14&times;15:1681"; the only number 1500..1799 on the page is 1681 |
| r strictly below min over Perminov ZT/Z/Q | met | row "`13x14x15` \|  1681 (?)   \| 1681 (1714)  \| 1681 (1714)": minimum 1681. The parenthesised 1714 values are higher and do not lower the bar |
| r strictly below lowest MerlijnW70 rank | met, vacuously | no file for any permutation of 13x14x15 in SHA256SUMS or in the full tree (truncated false, 39 entries). With no entry there is no bar. The nearest superset there, 13x14x16 m1805, is above 1644 anyway |
| "every one re-fetched live immediately before claiming" | met | the claim's pre-panel re-fetch was at 2026-10-28T22:08:49Z. My re-fetch at 22:33:28Z to 22:33:29Z returned byte-identical bodies (same sha256) for all five URLs |
| exact arithmetic over the claimed ring (Q) | met | two independent exact checks (section 3) |
| GF(2) clause | not triggered | the scheme is valid over Q. It uses denominators 2, 4, 5, 8, 10, 17, 20, 34, 40, 136, 272 and 1088 (counted from the files), so it is not a GF(2)-only scheme |
| composition, padding, block-splitting clause | not triggered | the clause bites only "if the resulting rank equals a value already listed". 1644 equals no value in any source I read. The construction is restriction of LITA's 15x15x15 rank-1977 scheme plus exact absorption, so it is more than plain padding |
| ternary/integer re-derivation exclusion | not applicable | new rank, not a ring upgrade at an existing rank |
| fewer-additions exclusion | not applicable | rank claim |
| POLICY rule 1 (comparator includes what is merged here) | met | merged objects for this cell in the pinned repo are known-knowns/faster-matrix-multiplication/schemes/13x14x15_r1677_Q.json and .../2026-10-15-anonymous-c6d1e0ab-49ee1c4f/object/13x14x15_r1645_Q.json (sha256 49ee1c4f6642..., byte-identical to claim/the-record-we-beat/13x14x15_r1645_Q.json, "m": 1645). 1644 < 1645. No other merged object for any permutation of 13,14,15 |
| POLICY rule 3 (equal or better value already public) | not triggered in what I read | the four sources and this repository have nothing at or below 1644 for this cell. Superset formats give nothing at or below 1644 either: on Perminov's ranks.md and fmm_sota.json, 13x14x16 is 1796, 13x15x15 1776, 14x14x15 1789/1790 and 14x15x15 1848. I did not scan pull requests or the literature (other skeptics) |
| POLICY rule 4 (strictly better value at review time supersedes) | not triggered in what I read | same sources, re-fetched at 22:33Z |

Margin: 1644 is 1 below the merged 1645 and 37 below the minimum (1681) over the four criterion sources.

### Hidden quantifiers and stretched definitions

- "STRICTLY LESS than ALL of": four sources plus the repository's merged value, all checked; strict in every case.
- "number of rank-one terms r": 1644 terms, no zero factor and no explicit zero coefficient. No two terms share two
  proportional factors, so no pair merges into one term. I checked the uv, uw and vw directions after normalization,
  with 0 mergeable pairs in each.
- "for a format": the object is for <14,15,13>, not the sorted (13,14,15). Rank is invariant under permuting the
  dimensions. The matrix multiplication tensor sum A_ij B_jl Z_li is unchanged by a cyclic relabelling of its three
  factors, and transposition (AB)^T = B^T A^T covers the rest. So a rank-r scheme for <14,15,13> gives a rank-r scheme
  for <13,14,15> by the cyclic shift (n,m,p) to (p,n,m), with no transpose needed. The bank's own
  verification_method and pitfalls say to compare against the sorted format for this reason. I did not rely on the
  argument alone. I built the permuted scheme explicitly (scripts/cyclic.py: u''[l*14+i] = w[i*13+l],
  v''[i*15+j] = u[i*15+j], w''[l*15+j] = v[j*13+l]) and verified it exactly as <13,14,15> (section 3).

## 3. Object verification

- sha256 (my computation): u.txt caef7bb7a297..., v.txt b31e5e77899a..., w.txt 79b90daf911f... (they match
  REPRODUCE.md).
- `sh verify-it-yourself/run_checks.sh` from a workspace copy (claimcopy/): "format <14,15,13>, 1644 terms, every
  term with three nonzero factors, common denominator 54400, 7452900 Brent equations checked, 0 wrong", then random
  exact evaluation with 0 of 182 entries wrong in each of 3 trials, and final PASS. Time 9.25 s.
- Independent check (scripts/mycheck.py, my own code). Each factor is scaled to integers, and all 7452900 Brent
  coefficients are computed as an integer identity modulo two primes, 1048573 and 1048571. Their product exceeds
  2 x the coefficient bound (33 bits), so by the Chinese remainder theorem the identity holds exactly over Q. Result:
  0 wrong coefficients for both primes, 1644 terms, 0 zero factors. A negative control (one W coefficient changed
  from 1 to 2 in a copy) makes the check fail, so the checker is not vacuous.
- The same independent check on the explicitly permuted <13,14,15> scheme (sorted/) also gives 0 wrong for both
  primes, with 1644 terms and 0 zero factors.

## 4. Fetches (one plain GET each, User-Agent "V3R1T4S-panel criterion skeptic (curl)", no cookies, no retries)

| time (UTC) | HTTP | sha256 | bytes | URL | value for (13,14,15) |
|---|---|---|---|---|---|
| 2026-10-28T22:33:28Z | 200 | d2a562a11c213effc7df98468757cda923925f248fab408ed38c485039851158 | 33137 | https://fmm.univ-lille.fr/13x14x15.html | 1681 |
| 2026-10-28T22:33:28Z | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | 343774 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 1681 (createdAt 2026-10-19T20:46:33) |
| 2026-10-28T22:33:28Z | 200 | 5f433497fdc4ea056f0d13e5adfdb22b70237ea23170134fe1a3d9637bb5f4bb | 52950 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | ZT 1681 (?), Z 1681 (1714), Q 1681 (1714): minimum 1681 |
| 2026-10-28T22:33:29Z | 200 | de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd | 3044 | https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS | no entry |
| 2026-10-28T22:33:29Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 11852 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | no entry (truncated false) |

All five hashes equal those in claim/TABLE_RECORD.md. I sent no pull-request or search API requests.

## 5. Null models

No null test is needed. The claim concerns one explicit object checked by a deterministic exact identity (the Brent
equations over Q), not a statistical or search-based result, so there is no chance level to beat. The relevant
controls are a negative control showing the checker can fail (done: one perturbed coefficient makes it fail) and a
check that the rank is not trivially implied by a known scheme for a superset format (done: the lowest superset value
listed is 1776, above 1644).

## Blocks

None. Every request returned HTTP 200, and there were no guard or classifier blocks.

text addressed to reviewers: none seen in claim/CLAIM.md, TABLE_RECORD.md, REPRODUCE.md or the fetched sources.

confirmed_scope: The files object/u.txt (sha256 caef7bb7...), object/v.txt (b31e5e77...) and object/w.txt (79b90daf...) define a bilinear scheme over Q with exactly 1644 rank-one terms and no zero factors that satisfies all 7452900 Brent equations for <14,15,13> in exact arithmetic (and, after the cyclic relabelling, for <13,14,15>), which is strictly below the rank 1681 that fmm_sota.json, the Lille page 13x14x15.html and the minimum of Perminov's ZT/Z/Q columns in docs/ranks.md each list for (13,14,15) as re-fetched at 2026-10-28T22:33Z, strictly below the rank 1645 merged in this repository, and in a cell where MerlijnW70/fmm-schemes lists no scheme.

Verdict: the full main success criterion is met literally. The result is a genuine strict improvement, not subsumed
by any listed value or superset format I read, and no partial win is involved. Novelty against pull requests and the
literature is left to the other skeptics.

pass: true
