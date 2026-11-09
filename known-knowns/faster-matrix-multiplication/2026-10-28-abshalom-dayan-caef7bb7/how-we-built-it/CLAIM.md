# Claim

**Claim (one sentence):** The three files in `object/` (u.txt, v.txt, w.txt) define a bilinear (non-commutative)
scheme over Q with exactly 1644 multiplications for the matrix multiplication format <14,15,13> (A 14x15 times
B 15x13), a permutation of the sorted format <13,14,15>, and 1644 is strictly below the minimum 1681 of the four
sources the criterion names (fmm_sota.json 1681, the Lille page https://fmm.univ-lille.fr/13x14x15.html 1681,
Perminov's docs/ranks.md ZT 1681 (?), Z 1681 (1714), Q 1681 (1714), MerlijnW70/fmm-schemes no entry) and strictly
below the rank 1645 merged in this repository for <13,14,15> (pull request #166); see TABLE_RECORD.md.

- target id: `fmm-catalogue-small-format-rank`
- claimed level: the main success criterion (max(n,m,p) = 15 <= 16; sorted format (13,14,15) is not (3,3,3) or
  (4,4,4)). Rank is invariant under permuting the three dimensions of a bilinear scheme (cyclic permutations and
  transposition), so a scheme for <14,15,13> gives one of the same rank for <13,14,15>.
- status_source (from the bank entry): https://fmm.univ-lille.fr/
- comparator also includes what is merged in this repository (repo kit/POLICY.md, fast matrix multiplication rule 1):
  <13,14,15> rank 1645 (pull request #166, merged 2026-10-15); a copy is in `the-record-we-beat/13x14x15_r1645_Q.json`
  (encoding vocab_rle_v1, Perminov convention: w index l*n1+i).
- ring: Q (coefficients are integers and fractions; denominators occurring: 2, 4, 5, 8, 10, 17, 20, 34, 40, 136, 272,
  1088; least common denominator 5440; check_scheme.py scales by 54400, also a common denominator).
- provenance (fact, for the composition clause): obtained from the published 15x15x15 rank-1977 scheme of Khoruzhii,
  Serafin, Gelss and Pokutta (LITA, https://github.com/khoruzhii/lita, file schemes/15x15x15_r1977.npz, copied in
  `rebuild/`) by three exact one-slice restrictions, each followed by exact absorption of linearly dependent terms:
  (1) the row index shared by A and C: 1977 -> 1865 terms, absorption -> 1836 (14x15x15);
  (2) the column index shared by B and C: -> 1709 (14x15x14), nothing absorbed;
  (3) the same axis again: -> 1677, absorption of 33 -> 1644 (14x15x13).
  `rebuild/` regenerates the object byte for byte. It is not a composition, padding or block splitting of known
  schemes.

## Success criterion (verbatim from the bank)

Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format <n,m,p> with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

## Partial wins (verbatim from the bank)

- p1: {'id': 'p1', 'statement': "A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column."}
- p2: {'id': 'p2', 'statement': "A GF(2)-only improvement: an exactly verified (mod 2) scheme whose rank is strictly below the F2 column for its format in the live matmulcatalog COVERAGE.md AND below every GF(2)-valid scheme for that format in Perminov's live repository and MerlijnW70's repository, for a format where the characteristic-0 best rank is already <= the new GF(2) rank (so it is not a new rank overall)."}
