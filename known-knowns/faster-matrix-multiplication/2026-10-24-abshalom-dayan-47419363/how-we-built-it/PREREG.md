# PREREG (frozen 2026-10-24T16:14:48Z, from date -u)

(Package copy of the run's PREREG.md, otherwise unchanged: the per-format URL template in the criterion is written
with braces here, fmm.univ-lille.fr/{n}x{m}x{p}.html, because the package checker reads the angle-bracket form as an
unfilled placeholder.)

## Criterion (verbatim)
Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format <n,m,p> with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

## Partial wins (verbatim)
- p1: A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column.
- p2: A GF(2)-only improvement: an exactly verified (mod 2) scheme whose rank is strictly below the F2 column for its format in the live matmulcatalog COVERAGE.md AND below every GF(2)-valid scheme for that format in Perminov's live repository and MerlijnW70's repository, for a format where the characteristic-0 best rank is already <= the new GF(2) rank (so it is not a new rank overall).

## Statistic and checker
- Object: an explicit scheme file (JSON, rational coefficients as exact strings) for one sorted format.
- r = number of terms with all three factors nonzero, as counted by the checkers.
- Judged by BOTH exact checkers in attempts/evaluator-first/code/: check_stdlib.py (integer expansion of every term) and check_flint.py (exact fmpz slice products). Both must print PASS. Any disagreement kills the object.
- Bar for a format: the minimum of fmm_sota.json rank, the Lille per-format page rank, Perminov docs/ranks.md (min over ZT, Z, Q including bracketed values; the README table moved there on 2026-10-23) and MerlijnW70 SHA256SUMS ranks, plus any rank for that cell in this repo (known-knowns, open pull requests). All re-fetched live (one GET each) right before claiming.
- Threshold: r <= bar - 1 (strict). r == bar is a tie and is not a win.
- Main criterion only for max dim <= 16 and sorted format not (3,3,3) or (4,4,4). For max dim 17..32: partial win p1 only (fmm_sota.json and Lille page).
- One cell per claim. If several cells qualify, the one with the largest margin (bar - r), ties broken by smaller max dim, is panelled first; the others are reported as separate leads.

## Null design
null_test: not needed because the claim is an explicit object checked by two deterministic exact checkers against a table value (no search statistic, no chance baseline).

## Planned cells (decided before any scored output)
- <12,13,13> (bar 1274) from LITA 13^3; <14,14,14> (bar 1593) from LITA 15^3; <16,16,16> (bar 2236) from LITA 17^3; fallback p1 cells with max dim 17..32 next to odd LITA squares.
- Exploratory probe already run before this freeze (reported, not a claim): one slice of LITA 13^3 plus absorption gave 1275 for <12,13,13>, one above the bar.
