# Claim

**Claim (one sentence):** The three files in `object/` (u.txt, v.txt, w.txt) define a bilinear (non-commutative)
scheme over Q with exactly 1836 multiplications for the matrix multiplication format <14,15,15> (A 14x15 times
B 15x15), and 1836 is strictly below the minimum 1848 of the four sources the criterion names: fmm_sota.json lists
1848, the Lille per-format page https://fmm.univ-lille.fr/14x15x15.html lists 1890, Perminov's docs/ranks.md lists
ZT 1894, Z 1892, Q 1848, and MerlijnW70/fmm-schemes lists no <14,15,15> scheme (all fetched 2026-10-26T22:01Z; see
TABLE_RECORD.md).

- target id: `fmm-catalogue-small-format-rank`
- claimed level: the main success criterion (max(n,m,p) = 15 <= 16; sorted format (14,15,15) is not (3,3,3) or
  (4,4,4)).
- status_source (from the bank entry): https://fmm.univ-lille.fr/
- ring: Q (integer and fractional coefficients; common denominator 54400).
- also below every value already public in this repository: the merged known-knowns entry <14,15,15> rank 1842
  (TROPHY_CASE #44). See TABLE_RECORD.md, which also records that open pull request #752 (same contributor) names
  this rank-1836 <14,15,15> scheme as an unclaimed intermediate and ships code that rebuilds it.
- provenance (fact, for the composition clause): obtained from the published 15x15x15 rank-1977 scheme of
  Khoruzhii, Serafin, Gelss and Pokutta (LITA, https://github.com/khoruzhii/lita, file schemes/15x15x15_r1977.npz,
  copied in `rebuild/`) by one exact one-slice restriction of the row index shared by A and C, with
  e = (1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1) on the A side and f = (-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1) on the C side
  (1865 terms remain), followed by exact absorption of 29 terms (linear dependencies among the terms), 1836 remain.
  `rebuild/` regenerates the object byte for byte. It is not a composition, padding or block splitting of known
  schemes.

## Success criterion (verbatim from the bank)

Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format <n,m,p> with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).
