# Claim

**Claim (one sentence):** The three files in `object/` (u.txt, v.txt, w.txt) define a bilinear (non-commutative)
scheme over Q with exactly 1270 multiplications for the matrix multiplication format <12,13,13> (A 12x13 times
B 13x13), and 1270 is strictly below the minimum 1274 of the four sources the criterion names: fmm_sota.json lists
1274, the Lille per-format page https://fmm.univ-lille.fr/12x13x13.html lists 1274, Perminov's docs/ranks.md lists
ZT 1298 (?), Z 1298 (?), Q 1274, and MerlijnW70/fmm-schemes lists no <12,13,13> scheme (all fetched
2026-10-27T22:01Z and again at 22:05Z; see TABLE_RECORD.md).

- target id: `fmm-catalogue-small-format-rank`
- claimed level: the main success criterion (max(n,m,p) = 13 <= 16; sorted format (12,13,13) is not (3,3,3) or
  (4,4,4)).
- status_source (from the bank entry): https://fmm.univ-lille.fr/
- ring: Q (coefficients are integers and fractions; denominators occurring: 2, 3, 4, 6, 8, 12, 13, 16, 24, 32, 39,
  96, 117; common denominator of the Brent check 59904).
- nothing is merged in this repository for <12,13,13> or a permutation; see TABLE_RECORD.md.
- provenance (fact, for the composition clause): obtained from the published 13x13x13 rank-1379 scheme of
  Khoruzhii, Serafin, Gelss and Pokutta (LITA, https://github.com/khoruzhii/lita, file schemes/13x13x13_r1379.npz,
  copied in `rebuild/`) by one exact one-slice restriction of the row index shared by A and C, with
  e = (1,1,1,1,1,1,-4,1,1,1,1,1,1) on the A side and f = (-1,1,1,1,1,1,1,1,1,1,1,1,1) on the C side (84 terms vanish,
  1295 remain), followed by exact absorption of 25 terms (linear dependencies among the terms), 1270 remain.
  `rebuild/` regenerates the object byte for byte. It is not a composition, padding or block splitting of known
  schemes.

## Success criterion (verbatim from the bank)

Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format <n,m,p> with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

## Partial wins (verbatim from the bank)

- p1: A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column.
- p2: A GF(2)-only improvement: an exactly verified (mod 2) scheme whose rank is strictly below the F2 column for its format in the live matmulcatalog COVERAGE.md AND below every GF(2)-valid scheme for that format in Perminov's live repository and MerlijnW70's repository, for a format where the characteristic-0 best rank is already <= the new GF(2) rank (so it is not a new rank overall).
